# ginfo.py

import os
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import Message
from xeonmodz import app


@app.on_message(filters.command("ginfo"))
async def ginfo(_, message: Message):
    try:
        if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            return await message.reply_text("❌ This command only works in groups.")

        chat = await app.get_chat(message.chat.id)

        caption = (
            f"🏷 **Group Name:** {chat.title}\n"
            f"🆔 **Group ID:** `{chat.id}`\n"
            f"🔗 **Username:** @{chat.username if chat.username else 'None'}\n"
            f"👥 **Members:** {chat.members_count if getattr(chat, 'members_count', None) else 'Unknown'}\n\n"
            f"📝 **Description:**\n"
            f"{chat.description or 'No description set.'}"
        )

        if chat.photo:
            photo = await app.download_media(chat.photo.big_file_id)
            await message.reply_photo(photo, caption=caption)
            if os.path.exists(photo):
                os.remove(photo)
        else:
            await message.reply_text(caption)

    except Exception as e:
        await message.reply_text(f"❌ Error:\n`{e}`")