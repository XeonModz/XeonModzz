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

    try:
        member = await client.get_chat_member(
            message.chat.id,
            message.from_user.id
        )

        status = str(member.status).lower()

        if (
            "administrator" not in status
            and "creator" not in status
            and "owner" not in status
        ):
            return

    except:
        return

    if len(message.command) != 2:
        return await message.reply_text(
            "Usage:\n"
            "/antilink on\n"
            "/antilink off\n"
            "/antilink status"
        )

    mode = message.command[1].lower()

    if mode == "on":

        ENABLED_CHATS.add(message.chat.id)

        return await message.reply_text(
            "🔒 AntiLink Enabled"
        )

    elif mode == "off":

        ENABLED_CHATS.discard(message.chat.id)

        return await message.reply_text(
            "🔓 AntiLink Disabled"
        )

    elif mode == "status":

        if message.chat.id in ENABLED_CHATS:

            return await message.reply_text(
                "🔒 AntiLink Status: ENABLED"
            )

        else:

            return await message.reply_text(
                "🔓 AntiLink Status: DISABLED"
            )


@app.on_message(filters.group & filters.text, group=100)
async def anti_link_checker(client, message):

    if message.chat.id not in ENABLED_CHATS:
        return

    if not message.from_user:
        return

    # Allow owner/admins
    try:

        member = await client.get_chat_member(
            message.chat.id,
            message.from_user.id
        )

        status = str(member.status).lower()

        if (
            "administrator" in status
            or "creator" in status
            or "owner" in status
        ):
            return

    except:
        pass

    text = message.text or ""

    if text.startswith("/"):
        return

    # Delete forwarded messages
    if (
        getattr(message, "forward_from", None)
        or getattr(message, "forward_from_chat", None)
        or getattr(message, "forward_sender_name", None)
    ):

        try:
            await message.delete()
        except:
            pass

        return

    # Delete links/domains/subdomains
    if LINK_REGEX.search(text):

        try:
            await message.delete()
        except:
            pass