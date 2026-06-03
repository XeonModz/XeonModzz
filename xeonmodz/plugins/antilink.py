from pyrogram import filters
from xeonmodz import app
import re

ENABLED_CHATS = set()

LINK_REGEX = re.compile(
    r"(https?://|www\.|t\.me/|telegram\.me/|telegram\.dog/|discord\.gg/|discord\.com/invite/|(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})",
    re.IGNORECASE
)

print("ANTILINK PLUGIN LOADED")


@app.on_message(filters.command("antilink") & filters.group)
async def antilink_toggle(client, message):

    if len(message.command) != 2:
        return await message.reply_text(
            "Usage:\n/antilink on\n/antilink off"
        )

    mode = message.command[1].lower()

    if mode == "on":

        ENABLED_CHATS.add(message.chat.id)

        return await message.reply_text(
            "✅ AntiLink Enabled"
        )

    elif mode == "off":

        ENABLED_CHATS.discard(message.chat.id)

        return await message.reply_text(
            "❌ AntiLink Disabled"
        )


@app.on_message(filters.group & filters.text, group=100)
async def anti_link_checker(client, message):

    if message.chat.id not in ENABLED_CHATS:
        return

    if not message.from_user:
        return

    # Allow admins
    try:

        member = await client.get_chat_member(
            message.chat.id,
            message.from_user.id
        )

        if member.status in [
            "administrator",
            "creator"
        ]:
            return

    except:
        pass

    text = message.text or ""

    if text.startswith("/"):
        return

    # Forwarded message block
    if (
        message.forward_from
        or message.forward_from_chat
        or message.forward_sender_name
    ):

        try:
            await message.delete()
        except:
            pass

        return

    # Link block
    if LINK_REGEX.search(text):

        try:
            await message.delete()
        except:
            pass