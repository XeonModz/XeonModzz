from pyrogram import filters
from xeonmodz import app
from config import REMOVE_BG_API
import requests
import os


@app.on_message(filters.command(["rmbg", "removebg"]))
async def remove_bg(_, message):

    replied = message.reply_to_message

    if not replied:
        return await message.reply_text(
            "Reply to an image with /rmbg"
        )

    if not (replied.photo or replied.document):
        return await message.reply_text(
            "Reply to an image with /rmbg"
        )

    status = await message.reply_text(
        "⏳ Removing background..."
    )

    input_file = None
    output_file = f"rmbg_{message.id}.png"

    try:
        input_file = await replied.download()

        with open(input_file, "rb") as image:
            response = requests.post(
                "https://api.remove.bg/v1.0/removebg",
                files={"image_file": image},
                data={"size": "auto"},
                headers={"X-Api-Key": REMOVE_BG_API},
                timeout=120
            )

        if response.status_code != 200:
            return await status.edit(
                f"❌ API Error\n\n{response.text}"
            )

        with open(output_file, "wb") as out:
            out.write(response.content)

        await message.reply_document(
            output_file,
            caption="✨ Background Removed"
        )

        await status.delete()

    except Exception as e:
        await status.edit(
            f"❌ Error:\n`{e}`"
        )

    finally:
        if input_file and os.path.exists(input_file):
            os.remove(input_file)

        if os.path.exists(output_file):
            os.remove(output_file)