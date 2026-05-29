from pyrogram import Client, filters
from pyrogram.types import Message
from xeonmodz import app
from xeonmodz.lib.mode import isPrivate
import os


@app.on_message(filters.command("stickid"))
@isPrivate
async def sticker_id(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a sticker.")

    reply = message.reply_to_message

    if not reply.sticker:
        return await message.reply("That's not a sticker. Reply to a sticker.")

    await message.reply(
        f"🌒 Sticker ID:\n`{reply.sticker.file_id}`"
    )


@app.on_message(filters.command("sticker"))
@isPrivate
async def image_to_sticker(client: Client, message: Message):
    replied = message.reply_to_message

    if not replied:
        return await message.reply(
            "Reply to an image with /sticker"
        )

    if not (replied.photo or replied.document):
        return await message.reply(
            "Reply to an image with /sticker"
        )

    status = await message.reply("⏳ Creating sticker...")

    file_path = None
    sticker_path = "sticker.webp"

    try:
        file_path = await replied.download()

        os.system(
            f'ffmpeg -i "{file_path}" '
            f'-vf "scale=512:512:force_original_aspect_ratio=decrease" '
            f'"{sticker_path}" -y > /dev/null 2>&1'
        )

        await message.reply_sticker(sticker_path)
        await status.delete()

    except Exception as e:
        await status.edit(f"❌ Error:\n`{e}`")

    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

        if os.path.exists(sticker_path):
            os.remove(sticker_path)



