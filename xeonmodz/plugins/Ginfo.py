from pyrogram import Client, filters
from pyrogram.types import Message
import os

@Client.on_message(filters.command("ginfo"))
async def ginfo(client: Client, message: Message):
    if message.chat.type not in ["supergroup", "group"]:
        return await message.reply_text("❌ Use this command in a group.")

    chat = await client.get_chat(message.chat.id)

    caption = (
        f"🏷 **Group Name:** {chat.title}\n"
        f"🆔 **Group ID:** `{chat.id}`\n"
        f"🔗 **Username:** @{chat.username if chat.username else 'None'}\n\n"
        f"📝 **Description:**\n"
        f"{chat.description if chat.description else 'No description set.'}"
    )

    if chat.photo:
        photo = await client.download_media(chat.photo.big_file_id)
        await message.reply_photo(photo, caption=caption)
        try:
            os.remove(photo)
        except:
            pass
    else:
        await message.reply_text(caption)