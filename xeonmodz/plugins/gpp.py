# Version: 1.0 Beta
# ©️ 2025 xeonmodz ALL RIGHTS RESERVED
from pyrogram import Client, filters
from pyrogram.types import Message
from xeonmodz import app
from config import SUDO

@app.on_message(filters.command("gpp") & filters.group & filters.user(SUDO))
async def update_group_dp(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("Please reply to an image to update the group profile picture.")
        return

    if not message.reply_to_message.photo:
        await message.reply_text("Please reply to an image to update the group profile picture.")
        return
    
    photo = await message.reply_to_message.download()
    try:
        await client.set_chat_photo(chat_id=message.chat.id, photo=photo)
        await message.reply_text("Group profile picture updated successfully!")
    except Exception as e:
        await message.reply_text(f"Failed to update group profile picture: {e}")

@app.on_message(filters.command("pp") & filters.private & filters.user(SUDO))
async def update_personal_dp(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("Please reply to an image to update your profile picture.")
        return

    if not message.reply_to_message.photo:
        await message.reply_text("Please reply to an image to update your profile picture.")
        return
    
    photo = await message.reply_to_message.download()
    try:
        await client.set_profile_photo(photo=photo)
        await message.reply_text("Personal profile picture updated successfully!")
    except Exception as e:
        await message.reply_text(f"Failed to update profile picture: {e}")