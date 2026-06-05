from pyrogram import filters
from xeonmodz import app
from xeonmodz.lib.mode import isPrivate
from PIL import Image
import os

os.makedirs("downloads", exist_ok=True)

@app.on_message(filters.command(["crop512", "c512"]) & filters.reply)
@isPrivate
async def crop_512(client, message):

    status = await message.reply_text("✂️ Cropping to 512x512...")

    try:

        reply = message.reply_to_message

        if reply.photo:
            file_path = await reply.download(
                file_name=f"downloads/photo_{message.id}.jpg"
            )

        elif reply.sticker:
            file_path = await reply.download(
                file_name=f"downloads/sticker_{message.id}.webp"
            )

        elif reply.document:
            file_path = await reply.download(
                file_name=f"downloads/file_{message.id}"
            )

        else:
            return await status.edit(
                "❌ Reply to an image or sticker."
            )

        img = Image.open(file_path).convert("RGBA")

        width, height = img.size

        # Crop to square from center
        side = min(width, height)

        left = (width - side) // 2
        top = (height - side) // 2
        right = left + side
        bottom = top + side

        img = img.crop(
            (left, top, right, bottom)
        )

        # Resize cropped square to 512x512
        img = img.resize(
            (512, 512),
            Image.Resampling.LANCZOS
        )

        output = f"downloads/crop512_{message.id}.png"

        img.save(
            output,
            format="PNG"
        )

        await message.reply_document(
            output,
            caption="✅ Cropped to 512×512"
        )

        await status.delete()

        try:
            os.remove(file_path)
            os.remove(output)
        except:
            pass

    except Exception as e:

        await status.edit(
            f"❌ Error:\n{e}"
        )