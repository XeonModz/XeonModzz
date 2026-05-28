# Version: 1.0 Beta
# ©️ 2025 xeonmodz ALL RIGHTS RESERVED
from xeonmodz import app
from config import BOT_NAME
from xeonmodz.lib.mode import isPrivate
from pyrogram import filters, enums
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@app.on_message(filters.command('id'))
@isPrivate
async def showid(app, message):
    chat_type = message.chat.type

    if message.reply_to_message and message.reply_to_message.forward_from_chat:
        forwarded_chat = message.reply_to_message.forward_from_chat
        return await message.reply_text(
            f'**{BOT_NAME} **\nThe forwarded message is from **{forwarded_chat.title}**.\n📌 Channel ID: <code>{forwarded_chat.id}</code>.'
        )

    if chat_type == enums.ChatType.PRIVATE:
        await message.reply_text(
            f'**{BOT_NAME} **\nUser ID: <code>{message.from_user.id}</code>'
        )
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        await message.reply_text(
            f'**{BOT_NAME} **\nGroup ID: <code>{message.chat.id}</code>'
        )
    elif chat_type == enums.ChatType.CHANNEL:
        await message.reply_text(
            f'**{BOT_NAME} **\nChannel ID: <code>{message.chat.id}</code>'
        )

    logging.info("🏓 ID command received")
