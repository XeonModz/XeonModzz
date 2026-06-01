import os
import requests
from pyrogram import filters
from pyrogram.types import Message
from xeonmodz import app
from config import IMGBB_API_KEY


@app.on_message(filters.command("url"))
async def image_to_url(_, message: Message):

    replied = message.reply_to_message

    if not replied:
        return await message.reply_text(
            "❌ Reply to a photo or image document."
        )

    if not (replied.photo or replied.document):
        return await message.reply_text(
            "❌ Reply to a photo or image document."
        )

    status = await message.reply_text(
        "📤 Uploading image..."
    )

    file_path = None

    try:
        file_path = await replied.download()

        with open(file_path, "rb") as image:
            response = requests.post(
                "https://api.imgbb.com/1/upload",
                params={
                    "key": IMGBB_API_KEY
                },
                files={
                    "image": image
                },
                timeout=120
            )

        data = response.json()

        if not data.get("success"):
            return await status.edit_text(
                f"❌ Upload Failed\n\n`{data}`"
            )

        image_url = data["data"]["url"]

        await status.edit_text(
            f"🔗 **Image URL**\n\n`{image_url}`",
            disable_web_page_preview=True
        )

    except Exception as e:
        await status.edit_text(
            f"❌ Error:\n`{e}`"
        )

    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)