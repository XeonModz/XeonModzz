from pyrogram import Client, filters
from pyrogram.types import Message
from dotsermodz import app
from dotsermodz.lib.mode import isPrivate

@app.on_message(filters.command("stickid"))
@isPrivate
async def sticker_id(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply("Please reply to a sticker.")
        return

    reply = message.reply_to_message

    if not reply.sticker:
        await message.reply("That’s not a sticker. Please reply to a sticker.")
        return

    file_id = reply.sticker.file_id
    await message.reply(f"🌒Sticker id:\n`{file_id}`")




