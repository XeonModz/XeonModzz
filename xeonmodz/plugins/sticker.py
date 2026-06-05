from pyrogram import filters
from xeonmodz import app
from xeonmodz.lib.mode import isPrivate
from PIL import Image
import tempfile
import os


@app.on_message(filters.command(["sticker"]) & filters.reply)
@isPrivate
async def sticker_converter(client, message):

    status = await message.reply_text("🖼 Creating sticker...")

    try:

        reply = message.reply_to_message

        if reply.photo:
            image_path = await reply.download()

        elif (
            reply.document
            and reply.document.mime_type
            and reply.document.mime_type.startswith("image/")
        ):
            image_path = await reply.download()

        else:
            return await status.edit(
                "❌ Reply to a PNG/JPG image."
            )

        img = Image.open(image_path).convert("RGBA")
        img.thumbnail((512, 512))

        fd, sticker_path = tempfile.mkstemp(suffix=".webp")
        os.close(fd)

        img.save(sticker_path, "WEBP")

        with open(sticker_path, "rb") as sticker_file:
            await message.reply_sticker(
                sticker_file
            )

        await status.delete()

        try:
            os.remove(image_path)
            os.remove(sticker_path)
        except:
            pass

    except Exception as e:

        await status.edit(
            f"❌ Error:\n{e}"
        )