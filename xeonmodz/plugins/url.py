import os
import requests

from pyrogram import filters
from pyrogram.types import Message

from xeonmodz import app


def upload_to_gofile(file_path):
    # Get available server
    server_data = requests.get(
        "https://api.gofile.io/servers",
        timeout=30
    ).json()

    server = server_data["data"]["servers"][0]["name"]

    with open(file_path, "rb") as f:
        upload = requests.post(
            f"https://{server}.gofile.io/uploadFile",
            files={"file": f},
            timeout=600
        )

    data = upload.json()

    if data.get("status") != "ok":
        raise Exception(str(data))

    return data["data"]["downloadPage"]


@app.on_message(filters.command("url"))
async def media_to_url(_, message: Message):
    replied = message.reply_to_message

    if not replied:
        return await message.reply_text(
            "❌ Reply to a media file."
        )

    media = (
        replied.photo
        or replied.video
        or replied.audio
        or replied.document
        or replied.voice
        or replied.animation
        or replied.video_note
    )

    if not media:
        return await message.reply_text(
            "❌ Reply to a photo, video, audio, voice, animation, video note, or document."
        )

    status = await message.reply_text(
        "📤 Downloading media..."
    )

    file_path = None

    try:
        file_path = await replied.download()

        await status.edit_text(
            "☁️ Uploading to GoFile..."
        )

        url = upload_to_gofile(file_path)

        await status.edit_text(
            f"✅ Upload Successful\n\n"
            f"🔗 URL:\n`{url}`",
            disable_web_page_preview=True
        )

    except Exception as e:
        await status.edit_text(
            f"❌ Upload Failed\n\n`{e}`"
        )

    finally:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass