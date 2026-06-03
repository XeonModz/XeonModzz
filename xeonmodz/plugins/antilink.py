from pyrogram import filters
from pymongo import MongoClient
from xeonmodz import app
from config import MONGO_URL
import re

mongo = MongoClient(MONGO_URL)

db = mongo["XeonModz"]
collection = db["antilink"]

LINK_REGEX = re.compile(
    r"("
    r"https?://\S+|"
    r"www\.\S+|"
    r"(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}|"
    r"t\.me/\S+|"
    r"telegram\.me/\S+|"
    r"telegram\.dog/\S+|"
    r"discord\.gg/\S+|"
    r"discord\.com/invite/\S+|"
    r"bit\.ly/\S+|"
    r"tinyurl\.com/\S+|"
    r"goo\.gl/\S+|"
    r"@\w+"
    r")",
    re.IGNORECASE
)


def enabled(chat_id):
    return collection.find_one(
        {"chat_id": chat_id}
    ) is not None


@app.on_message(filters.command("antilink") & filters.group)
async def antilink_toggle(client, message):

    try:
        member = await client.get_chat_member(
            message.chat.id,
            message.from_user.id
        )

        if member.status not in [
            "creator",
            "administrator"
        ]:
            return

    except:
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n"
            "/antilink on\n"
            "/antilink off"
        )

    option = message.command[1].lower()

    if option == "on":

        collection.update_one(
            {"chat_id": message.chat.id},
            {"$set": {"chat_id": message.chat.id}},
            upsert=True
        )

        await message.reply_text(
            "🔒 AntiLink Enabled"
        )

    elif option == "off":

        collection.delete_one(
            {"chat_id": message.chat.id}
        )

        await message.reply_text(
            "🔓 AntiLink Disabled"
        )


@app.on_message(filters.group, group=100)
async def anti_link_checker(client, message):

    if not enabled(message.chat.id):
        return

    if not message.from_user:
        return

    # Admin bypass
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

    # Block forwarded messages
    if (
        message.forward_from_chat
        or message.forward_sender_name
        or message.forward_from
    ):
        try:
            await message.delete()
        except:
            pass
        return

    text = (
        message.text
        or message.caption
        or ""
    )

    found = False

    # Hidden telegram links
    if message.entities:
        for entity in message.entities:

            etype = str(entity.type).lower()

            if (
                "url" in etype
                or "text_link" in etype
                or "mention" in etype
            ):
                found = True
                break

    # Regex links/domains
    if LINK_REGEX.search(text):
        found = True

    if found:
        try:
            await message.delete()
        except:
            pass