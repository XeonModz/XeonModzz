# Version: 1.0
# Pinterest Downloader

from pyrogram import filters
from xeonmodz import app
from xeonmodz.lib.mode import isPrivate
from config import XEON_PIN_API
import requests


@app.on_message(filters.command("pin"))
@isPrivate
async def pinterest_downloader(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/pin pinterest_url"
        )

    query = message.command[1]

    api = f"{XEON_PIN_API}/pin?url={query}"

    try:

        response = requests.get(api)
        data = response.json()

    except Exception as e:

        return await message.reply_text(
            f"API Error:\n{e}"
        )

    if not data.get("status"):

        return await message.reply_text(
            "Failed to fetch Pinterest media."
        )

    creator = data.get("creator", "Unknown")

    videos = [
        vid for vid in data.get("videos", [])
        if isinstance(vid, str)
        and vid.startswith("http")
    ]

    for vid in videos:

        try:

            await message.reply_video(
                video=vid,
                caption=f"Downloaded from Pinterest\nCreator: {creator}"
            )

        except Exception as e:

            print(f"Video Error: {e}")

    images = [
        img for img in data.get("images", [])
        if isinstance(img, str)
        and img.startswith("http")
        and ".png)}" not in img
    ]

    for img in images:

        try:

            await message.reply_photo(
                photo=img,
                caption=f"Downloaded from Pinterest\nCreator: {creator}"
            )

        except Exception as e:

            print(f"Image Error: {e}")

    if not videos and not images:

        await message.reply_text(
            "No media found."
        )