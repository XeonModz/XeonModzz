# Version: 1.0 Beta
# ©️ 2025 XeonModz ALL RIGHTS RESERVED

from pyrogram import filters
from xeonmodz.lib.mode import isPrivate
from xeonmodz import app
import requests


# Instagram Downloader
@app.on_message(filters.command("insta"))
@isPrivate
async def insta_downloader(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Please provide an Instagram URL."
        )

    query = message.command[1]

    api = (
        "https://xeon-insta-api.onrender.com/"
        f"insta?url={query}"
    )

    try:

        response = requests.get(api)
        data = response.json()

    except Exception as e:

        return await message.reply_text(
            f"API Error:\n{e}"
        )

    if not data.get("status"):

        return await message.reply_text(
            "Failed to fetch Instagram media."
        )

    media = data.get("media")
    media_type = data.get("type")
    owner = data.get("owner", "Unknown")

    try:

        if media_type == "video":

            await message.reply_video(
                video=media,
                caption=(
                    f"Downloaded from Instagram\n"
                    f"Owner: {owner}"
                )
            )

        elif media_type == "image":

            await message.reply_photo(
                photo=media,
                caption=(
                    f"Downloaded from Instagram\n"
                    f"Owner: {owner}"
                )
            )

        else:

            await message.reply_text(
                "Unsupported media type."
            )

    except Exception as e:

        await message.reply_text(
            f"Error:\n{e}"
        )


# Pinterest Downloader
@app.on_message(filters.command("pin"))
@isPrivate
async def pinterest_downloader(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Please provide a Pinterest URL."
        )

    query = message.command[1]

    api = (
        "https://xeon-pin-api.onrender.com/"
        f"pin?url={query}"
    )

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

    # Videos
    videos = [
        vid for vid in data.get("videos", [])
        if isinstance(vid, str)
        and vid.startswith("http")
    ]

    for vid in videos:

        try:

            await message.reply_video(
                video=vid,
                caption=(
                    f"Downloaded from Pinterest\n"
                    f"Creator: {creator}"
                )
            )

        except Exception as e:

            print(f"Video Error: {e}")

    # Images
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
                caption=(
                    f"Downloaded from Pinterest\n"
                    f"Creator: {creator}"
                )
            )

        except Exception as e:

            print(f"Image Error: {e}")

    if not videos and not images:

        await message.reply_text(
            "No media found."
        )