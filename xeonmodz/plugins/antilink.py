from pyrogram import filters
from xeonmodz import app
from pymongo import MongoClient
from config import MONGO_URL
import re

mongo = MongoClient(MONGO_URL)

db = mongo["XeonModz"]
antilink_db = db["antilink"]

LINK_REGEX = re.compile(
    r"("
    r"https?://\S+|"
    r"www\.\S+|"
    r"t\.me/\S+|"
    r"telegram\.me/\S+|"
    r"telegram\.dog/\S+|"
    r"discord\.gg/\S+|"
    r"discord\.com/invite/\S+|"
    r"bit\.ly/\S+|"
    r"tinyurl\.com/\S+|"
    r"[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(/[^\s]*)?|"
    r"@[a-zA-Z0-9_]{5,}"
    r")",
    re.IGNORECASE
)


def is_enabled(chat_id):
    return antilink_db.find_one(
        {"chat_id": chat_id}
    ) is not None


@app.on_message(filters.command("antilink") & filters.group)
async def antilink_toggle(client, message):

    member = await client.get_chat_member(
        message.chat.id,
        message.from_user.id
    )

    if member.status not in ["creator", "administrator"]:
        return

    if len(message.command) != 2:

        return await message.reply_text(
            "Usage:\n"
            "/antilink on\n"
            "/antilink off"
        )

    mode = message.command[1].lower()

    if mode == "on":

        antilink_db.update_one(
            {"chat_id": message.chat.id},
            {"$set": {"chat_id": message.chat.id}},
            upsert=True
        )

        try:
            await message.react("✅")
        except:
            pass

        await message.reply_text(
            "🔒 AntiLink Enabled"
        )

    elif mode == "off":

        antilink_db.delete_one(
            {"chat_id": message.chat.id}
        )

        try:
            await message.react("❌")
        except:
            pass

        await message.reply_text(
            "🔓 AntiLink Disabled"
        )


@app.on_message(filters.group, group=100)
async def anti_link_checker(client, message):

    if not is_enabled(message.chat.id):
        return

    if not message.from_user:
        return

    # allow admins
    try:

        member = await client.get_chat_member(
            message.chat.id,
            message.from_user.id
        )

        if member.status in [
            "creator",
            "administrator"
        ]:
            return

    except:
        return

    text = (
        message.text
        or message.caption
        or ""
    )

    if not text:
        return

    if text.startswith("/"):
        return

    found = False

    # Telegram entities
    if message.entities:

        for entity in message.entities:

            if str(entity.type).lower() in [
                "url",
                "text_link",
                "mention"
            ]:
                found = True
                break

    # Regex detection
    if LINK_REGEX.search(text):
        found = True

    if found:

        try:
            await message.delete()
        except:
            pass