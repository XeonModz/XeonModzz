# Word Chain Game Plugin for XeonModz Bot
# Ported from Node.js (souravkl11) to Python/Pyrogram
# Compatible with XeonModz-V1 (Pyrogram-based bot)
#
# Commands:
#   /wcg        - Create a new game (starts 60s join window)
#   /wcgstart   - Manually start after enough players joined
#   /endwcg     - End the current game
#   /wcgstats   - Show game statistics
#
# Players join by sending "join" during the waiting phase.
# During active play, the current player must send a valid English
# word that starts with the required letter and meets the minimum
# length for the current difficulty level.
#
# Word list source: dwyl/english-words (GPL 3.0)

import asyncio
import random
import time

import aiohttp
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import Message

from xeonmodz import app

# ---------------------------------------------------------------------------
# Word list loading
# ---------------------------------------------------------------------------

WORD_LIST_URL = (
    "https://rawcdn.githack.com/dwyl/english-words/"
    "20f5cc9b3f0ccc8ce45d814c532b7c2031bba31c/words_alpha.txt"
)

WORD_SET: set[str] = set()

FALLBACK_WORDS = {
    "yes", "you", "your", "year", "young", "yellow", "yard", "yell",
    "yolk", "yarn", "key", "keep", "kind", "know", "king", "kick",
    "kill", "kiss", "knee", "knife", "art", "arm", "arc", "ace",
    "age", "aid", "aim", "air", "add", "act", "ant", "ape", "apt",
}


async def load_word_list():
    global WORD_SET
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(WORD_LIST_URL, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                text = await resp.text()
                words = {w.strip().lower() for w in text.splitlines() if len(w.strip()) >= 3}
                WORD_SET = words
                print(f"[WordChain] Loaded {len(WORD_SET)} words from URL.")
    except Exception as e:
        print(f"[WordChain] Failed to load word list: {e}. Using fallback.")
        WORD_SET = FALLBACK_WORDS


# ---------------------------------------------------------------------------
# Difficulty system
# ---------------------------------------------------------------------------

def get_dynamic_difficulty(total_words: int, player_count: int) -> dict:
    if player_count <= 2:
        thresholds = [5, 12, 24, 40, 60, 80]
    elif player_count == 3:
        thresholds = [6, 15, 30, 50, 75, 100]
    elif player_count == 4:
        thresholds = [7, 17, 35, 55, 80, 110]
    else:
        thresholds = [8, 20, 40, 65, 95, 130]

    levels = [
        {"min_length": 3, "time_limit": 40, "level": "Beginner"},
        {"min_length": 4, "time_limit": 35, "level": "Easy"},
        {"min_length": 4, "time_limit": 30, "level": "Medium"},
        {"min_length": 5, "time_limit": 25, "level": "Challenging"},
        {"min_length": 5, "time_limit": 20, "level": "Hard"},
        {"min_length": 6, "time_limit": 18, "level": "Expert"},
        {"min_length": 6, "time_limit": 15, "level": "Master"},
    ]

    for i, threshold in enumerate(thresholds):
        if total_words < threshold:
            return levels[i]
    return levels[-1]


DIFFICULTY_EMOJI = {
    "Beginner": "🟢",
    "Easy": "🟡",
    "Medium": "🟠",
    "Challenging": "🔴",
    "Hard": "🟤",
    "Expert": "🟣",
    "Master": "⚫",
}


# ---------------------------------------------------------------------------
# Game state
# ---------------------------------------------------------------------------

class Player:
    def __init__(self, user_id: int, username: str):
        self.id = user_id
        self.username = username
        self.words = 0
        self.eliminated = False


class WordChainGame:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.players: list[Player] = []
        self.current_player_index = 0
        self.state = "waiting"          # waiting | active | finished
        self.current_letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.used_words: set[str] = set()
        self.total_words = 0
        self.longest_word = ""
        self.longest_word_player = ""
        self.start_time: float | None = None
        self.difficulty = get_dynamic_difficulty(0, 2)
        self.processing = False
        self.turn_number = 0
        # asyncio tasks / handles
        self._turn_task: asyncio.Task | None = None
        self._join_task: asyncio.Task | None = None

    # ------------------------------------------------------------------
    # Player helpers
    # ------------------------------------------------------------------

    def add_player(self, user_id: int, username: str) -> bool:
        if any(p.id == user_id for p in self.players):
            return False
        self.players.append(Player(user_id, username))
        return True

    def active_players(self) -> list[Player]:
        return [p for p in self.players if not p.eliminated]

    def current_player(self) -> Player | None:
        active = self.active_players()
        if not active:
            return None
        return active[self.current_player_index % len(active)]

    def next_player(self) -> Player | None:
        active = self.active_players()
        if not active:
            return None
        return active[(self.current_player_index + 1) % len(active)]

    def advance_turn(self):
        active = self.active_players()
        self.current_player_index = (self.current_player_index + 1) % max(len(active), 1)
        self.turn_number += 1

    def eliminate(self, user_id: int) -> bool:
        player = next((p for p in self.players if p.id == user_id), None)
        if not player or player.eliminated:
            return False
        player.eliminated = True
        active = self.active_players()
        if active:
            self.current_player_index = self.current_player_index % len(active)
        return True

    # ------------------------------------------------------------------
    # Difficulty
    # ------------------------------------------------------------------

    def update_difficulty(self) -> bool:
        old = self.difficulty["level"]
        self.difficulty = get_dynamic_difficulty(self.total_words, len(self.active_players()))
        return old != self.difficulty["level"]

    def diff_emoji(self) -> str:
        return DIFFICULTY_EMOJI.get(self.difficulty["level"], "🔵")

    def progress_info(self) -> str:
        n = len(self.active_players())
        if n <= 2:
            thresholds = [5, 12, 24, 40, 60, 80]
        elif n == 3:
            thresholds = [6, 15, 30, 50, 75, 100]
        elif n == 4:
            thresholds = [7, 17, 35, 55, 80, 110]
        else:
            thresholds = [8, 20, 40, 65, 95, 130]
        nxt = next((t for t in thresholds if t > self.total_words), None)
        return "MAX LEVEL" if nxt is None else f"{nxt - self.total_words} words to next level"

    def is_valid_word(self, word: str) -> bool:
        return word.lower() in WORD_SET

    # ------------------------------------------------------------------
    # Duration
    # ------------------------------------------------------------------

    def game_duration(self) -> str:
        if not self.start_time:
            return "00:00:00"
        secs = int(time.time() - self.start_time)
        h, rem = divmod(secs, 3600)
        m, s = divmod(rem, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    # ------------------------------------------------------------------
    # Timer management
    # ------------------------------------------------------------------

    def cancel_turn_timer(self):
        if self._turn_task and not self._turn_task.done():
            self._turn_task.cancel()
        self._turn_task = None

    def cancel_join_timer(self):
        if self._join_task and not self._join_task.done():
            self._join_task.cancel()
        self._join_task = None

    def cancel_all(self):
        self.cancel_turn_timer()
        self.cancel_join_timer()


# Active games: chat_id -> WordChainGame
active_games: dict[int, WordChainGame] = {}


# ---------------------------------------------------------------------------
# Message helpers
# ---------------------------------------------------------------------------

def mention(user: Player) -> str:
    return f"[{user.username}](tg://user?id={user.id})"


def status_message(game: WordChainGame) -> str:
    active = game.active_players()

    if len(active) <= 1:
        winner = active[0] if active else None
        lines = []
        if winner:
            lines.append(f"{mention(winner)} **Won** 🏆")
        else:
            lines.append("Game Over! No winner 😔")
        lines.append(f"Words: **{game.total_words}**")
        lines.append(f"Final Level: {game.diff_emoji()} **{game.difficulty['level']}**")
        if game.longest_word:
            lines.append(
                f"Longest word: **{game.longest_word} ({len(game.longest_word)})** "
                f"by {game.longest_word_player} 📚"
            )
        lines.append(f"Time: **{game.game_duration()}** ⏱️")
        return "\n".join(lines)

    cur = game.current_player()
    nxt = game.next_player()
    if not cur or not nxt:
        return "❌ Game error: No valid players found."

    return (
        f"🎲 Turn: {mention(cur)}\n"
        f"🙌 Next: {mention(nxt)}\n"
        f"🆎 Your word must start with **{game.current_letter}** "
        f"and have at least **{game.difficulty['min_length']}** letters\n"
        f"{game.diff_emoji()} Level: **{game.difficulty['level']}** ({game.progress_info()})\n"
        f"🏆 Players remaining: {len(active)}/{len(game.players)}\n"
        f"⏳ You have **{game.difficulty['time_limit']}s** to answer\n"
        f"📝 Total words: {game.total_words}"
    )


# ---------------------------------------------------------------------------
# Turn timer
# ---------------------------------------------------------------------------

async def run_turn_timer(game: WordChainGame, current_turn: int):
    """Sleeps for the current time limit, then eliminates the current player."""
    await asyncio.sleep(game.difficulty["time_limit"])

    # If the turn has already advanced, bail out
    if game.turn_number != current_turn or game.processing:
        return

    cur = game.current_player()
    if not cur:
        return

    await app.send_message(
        game.chat_id,
        f"{mention(cur)} ran out of time! They're out! 🚫",
        disable_web_page_preview=True,
    )

    game.eliminate(cur.id)
    active = game.active_players()

    if len(active) <= 1:
        msg = status_message(game)
        await app.send_message(game.chat_id, msg, disable_web_page_preview=True)
        game.cancel_all()
        active_games.pop(game.chat_id, None)
    else:
        game.advance_turn()
        msg = status_message(game)
        await app.send_message(game.chat_id, msg, disable_web_page_preview=True)
        start_turn_timer(game)


def start_turn_timer(game: WordChainGame):
    game.cancel_turn_timer()
    game.turn_number += 1
    current_turn = game.turn_number
    game._turn_task = asyncio.create_task(run_turn_timer(game, current_turn))


# ---------------------------------------------------------------------------
# /wcg  — create game
# ---------------------------------------------------------------------------

@app.on_message(filters.command("wcg") & filters.group)
async def cmd_wcg(_, message: Message):
    chat_id = message.chat.id

    if chat_id in active_games:
        return await message.reply_text("❌ A game is already active in this chat!")

    # Ensure word list is loaded
    if not WORD_SET:
        await message.reply_text("⏳ Loading word list, please wait...")
        await load_word_list()

    game = WordChainGame(chat_id)
    active_games[chat_id] = game

    await message.reply_text(
        "🎮 **Dynamic Word Chain Game Starting...**\n"
        "👥 Needs 2 or more players 🙋‍♂️🙋‍♀️\n"
        "⏳ Type **join** — 60 seconds to join ⏳\n"
        "🔄 *Difficulty increases automatically as you play!*\n"
        "🟢 Start: 3+ letters, 40s per turn\n"
        "⚫ Master: 6+ letters, 15s per turn\n"
        "⚡ *Fewer players = Faster level progression!*\n"
        "📊 *2 players: Every 5-12-24… words*\n"
        "📊 *3 players: Every 6-15-30… words*\n"
        "📊 *4+ players: Every 8-20-40… words*",
        disable_web_page_preview=True,
    )

    async def join_countdown():
        for remaining in [45, 30, 15]:
            await asyncio.sleep(15)
            if game.state != "waiting" or chat_id not in active_games:
                return
            txt = (
                f"🎮 Game starts in **{remaining}** seconds ⏳\n"
                f"Type **join** to play 🙋‍♂️🙋‍♀️\n"
                f"🔄 Dynamic difficulty system\n"
                f"⚡ Fewer players = Faster progression"
            )
            if game.players:
                txt += f"\n👥 {len(game.players)} player(s) joined."
            await app.send_message(chat_id, txt, disable_web_page_preview=True)

        # Time's up
        await asyncio.sleep(15)
        if game.state != "waiting" or chat_id not in active_games:
            return

        if len(game.players) >= 2:
            await _start_game(game)
        else:
            await app.send_message(chat_id, "❌ Not enough players joined! Game cancelled.")
            active_games.pop(chat_id, None)

    game._join_task = asyncio.create_task(join_countdown())


# ---------------------------------------------------------------------------
# /wcgstart — manual start
# ---------------------------------------------------------------------------

@app.on_message(filters.command("wcgstart") & filters.group)
async def cmd_wcgstart(_, message: Message):
    chat_id = message.chat.id
    game = active_games.get(chat_id)

    if not game:
        return await message.reply_text("❌ No game to start! Use /wcg to create one first.")
    if game.state != "waiting":
        return await message.reply_text("❌ Game is already running or finished!")
    if len(game.players) < 2:
        return await message.reply_text("❌ Need at least 2 players to start!")

    game.cancel_join_timer()
    await _start_game(game)


async def _start_game(game: WordChainGame):
    game.state = "active"
    game.start_time = time.time()
    game.turn_number = 0
    game.update_difficulty()
    msg = status_message(game)
    await app.send_message(game.chat_id, msg, disable_web_page_preview=True)
    start_turn_timer(game)


# ---------------------------------------------------------------------------
# /endwcg — force end
# ---------------------------------------------------------------------------

@app.on_message(filters.command("endwcg") & filters.group)
async def cmd_endwcg(_, message: Message):
    chat_id = message.chat.id
    game = active_games.pop(chat_id, None)

    if not game:
        return await message.reply_text("❌ No active game in this chat!")

    game.cancel_all()
    await message.reply_text("🛑 Word Chain Game ended by admin!")


# ---------------------------------------------------------------------------
# /wcgstats — show stats
# ---------------------------------------------------------------------------

@app.on_message(filters.command("wcgstats") & filters.group)
async def cmd_wcgstats(_, message: Message):
    chat_id = message.chat.id
    game = active_games.get(chat_id)

    if not game:
        return await message.reply_text("❌ No active game in this chat!")

    lines = [
        "📊 **Word Chain Game Stats**\n",
        f"🎮 State: {game.state}",
        f"{game.diff_emoji()} Level: {game.difficulty['level']}",
        f"📏 Min Length: {game.difficulty['min_length']} letters",
        f"⏱️ Time Limit: {game.difficulty['time_limit']}s",
        f"👥 Total Players: {len(game.players)}",
        f"🏆 Active Players: {len(game.active_players())}",
        f"📝 Words Used: {game.total_words}",
        f"🎯 Progress: {game.progress_info()}",
    ]
    if game.longest_word:
        lines.append(f"📏 Longest word: {game.longest_word} ({len(game.longest_word)})")
    if game.state == "active":
        lines.append(f"🔤 Current letter: {game.current_letter}")
        lines.append(f"⏱️ Duration: {game.game_duration()}")
        lines.append(f"🎯 Turn: {game.turn_number}")

    await message.reply_text("\n".join(lines), disable_web_page_preview=True)


# ---------------------------------------------------------------------------
# Reaction helper — pyrofork supports message.react()
# Falls back silently if the chat doesn't allow reactions
# ---------------------------------------------------------------------------

async def react(message: Message, emoji: str):
    try:
        await message.react(emoji)
    except Exception:
        pass  # Silently ignore if reactions aren't allowed in the chat


# ---------------------------------------------------------------------------
# Incoming text handler — join + word submission
# ---------------------------------------------------------------------------

@app.on_message(filters.text & filters.group & ~filters.command([
    "wcg", "wcgstart", "endwcg", "wcgstats"
]))
async def handle_text(_, message: Message):
    chat_id = message.chat.id
    game = active_games.get(chat_id)
    if not game:
        return

    user = message.from_user
    if not user:
        return

    user_id = user.id
    username = user.username or user.first_name or str(user_id)
    text = (message.text or "").strip().lower()

    # --- Join phase ---
    if text == "join" and game.state == "waiting":
        if game.add_player(user_id, username):
            await react(message, "👏")
        else:
            await react(message, "👀")  # Already joined
        return

    # --- Active game word submission ---
    if game.state != "active":
        return

    cur = game.current_player()
    if not cur or cur.id != user_id:
        return  # Not this player's turn

    if game.processing:
        return

    game.processing = True
    try:
        word = text.strip()

        if not word.isalpha():
            return  # Ignore messages with non-alpha chars silently

        if word[0].upper() != game.current_letter:
            await react(message, "❌")
            return

        if len(word) < game.difficulty["min_length"]:
            await react(message, "❌")
            return

        if word in game.used_words:
            await react(message, "🔄")
            return

        if not game.is_valid_word(word):
            await react(message, "🤔")
            return

        # Valid word — accept it
        game.cancel_turn_timer()

        game.used_words.add(word)
        game.total_words += 1

        # Find the Player object for cur to update word count
        p = next((pl for pl in game.players if pl.id == cur.id), None)
        if p:
            p.words += 1

        new_longest = False
        if len(word) > len(game.longest_word):
            game.longest_word = word
            game.longest_word_player = f"[{cur.username}](tg://user?id={cur.id})"
            new_longest = True

        level_changed = game.update_difficulty()
        game.current_letter = word[-1].upper()
        game.advance_turn()

        # React on the accepted word
        await react(message, "🏆" if new_longest else "✅")

        if level_changed:
            await app.send_message(
                chat_id,
                f"🆙 **LEVEL UP!** {game.diff_emoji()}\n"
                f"New Level: **{game.difficulty['level']}**\n"
                f"Min Length: **{game.difficulty['min_length']}** letters\n"
                f"Time Limit: **{game.difficulty['time_limit']}s** per turn\n"
                f"Progress: {game.progress_info()}",
                disable_web_page_preview=True,
            )

        msg = status_message(game)
        await app.send_message(chat_id, msg, disable_web_page_preview=True)
        start_turn_timer(game)

    finally:
        game.processing = False


# ---------------------------------------------------------------------------
# Load word list on startup
# ---------------------------------------------------------------------------

async def _init_words():
    await load_word_list()

# Schedule word list loading when the event loop starts
asyncio.get_event_loop().create_task(_init_words())