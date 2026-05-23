# Version: 1.0 Beta
# ©️ 2025 DOTSERMODZ ALL RIGHTS RESERVED
from pyrogram import Client, filters
from pyrogram.types import Message
from dotsermodz import app
from dotsermodz.lib.mode import isPrivate
from dotsermodz.lib.download import upload_to_catbox

# This command will upload the replied image to Catbox and return the URL
# Usage: /url or /upload
"""
@app.on_message(filters.command(["url", "upload"]))
@isPrivate
async def upload_image(client: Client, message: Message):
    if message.reply_to_message and message.reply_to_message.photo:
        photo = message.reply_to_message.photo
        file_path = await client.download_media(photo)
        url = upload_to_catbox(file_path)
        await message.reply(f"Here is your Url: \n` {url} `")
    else:
        await message.reply("Please reply to an image to upload.")

"""
@app.on_message(filters.command(["url", "upload"]))
@isPrivate
async def upload_image(client: Client, message: Message):
    if message.reply_to_message:
        media = None

        if message.reply_to_message.photo:
            media = message.reply_to_message.photo
        elif message.reply_to_message.document:
            media = message.reply_to_message.document
        elif message.reply_to_message.video:
            media = message.reply_to_message.video
        elif message.reply_to_message.audio:
            media = message.reply_to_message.audio
        elif message.reply_to_message.voice:
            media = message.reply_to_message.voice
        elif message.reply_to_message.video_note:
            media = message.reply_to_message.video_note
        else:
            return await message.reply("Unsupported media type. Please reply to a valid media message.")

        try:
            file_path = await client.download_media(media)
            url = upload_to_catbox(file_path)
            await message.reply(f"Here is your URL: \n`{url}`")
        except Exception as e:
            await message.reply(f"❌ Failed to upload: `{e}`")
    else:
        await message.reply("Please reply to a media message to upload.")
