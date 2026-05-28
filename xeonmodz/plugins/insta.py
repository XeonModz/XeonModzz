# Version: 1.0
# Instagram Downloader

from pyrogram import filters
from xeonmodz import app
from xeonmodz.lib.mode import isPrivate
from config import XEON_INSTA_API
import requests


@app.on_message(filters.command("insta"))
@isPrivate
async def insta_downloader(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/insta instagram_url"
        )

    query = message.command[1]

    api = f"{XEON_INSTA_API}/insta?url={query}"

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
                caption=f"Downloaded from Instagram\nOwner: {owner}"
            )

        elif media_type == "image":

            await message.reply_photo(
                photo=media,
                caption=f"Downloaded from Instagram\nOwner: {owner}"
            )

        else:

            await message.reply_text(
                "Unsupported media type."
            )

    except Exception as e:

        await message.reply_text(
            f"Error:\n{e}"
        )