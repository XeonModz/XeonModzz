from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from xeonmodz import app


@app.on_message(filters.command(["all", "tagall"]))
async def tag_all(_, message: Message):

    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return await message.reply_text(
            "❌ This command can only be used in groups."
        )

    reason = ""

    if len(message.command) > 1:
        reason = message.text.split(None, 1)[1]

    count = 0
    number = 1
    text = ""

    if reason:
        text += f"📢 **{reason}**\n\n"

    async for member in app.get_chat_members(message.chat.id):
        user = member.user

        if user.is_deleted:
            continue

        text += (
            f"{number} ➠ "
            f"[{user.first_name}](tg://user?id={user.id})\n"
        )

        number += 1
        count += 1

        if count == 10:
            await message.reply_text(
                text,
                disable_web_page_preview=True
            )

            text = ""
            count = 0

    if text:
        await message.reply_text(
            text,
            disable_web_page_preview=True
        )