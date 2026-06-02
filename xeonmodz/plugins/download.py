from pyrogram import filters
from xeonmodz.lib.mode import isPrivate
from xeonmodz import app
import requests


# Instagram Downloader
# Pinterest Downloader
@app.on_message(filters.command("pin"))
@isPrivate
async def pinterest_downloader(client, message):

    try:
        await message.react("⚡")
    except Exception:
        pass

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/pin pinterest_url"
        )

    query = message.command[1]

    try:

        response = requests.get(
            f"https://xeon-pin-api.onrender.com/pin?url={query}",
            timeout=30
        )

        data = response.json()

    except Exception as e:

        return await message.reply_text(
            f"API Error:\n{e}"
        )

    if not data.get("success"):

        return await message.reply_text(
            "Failed to fetch Pinterest media."
        )

    videos = data.get("videos", [])
    images = data.get("images", [])

    try:

        if videos:

            await message.reply_video(
                video=videos[0],
                caption="𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳"
            )

        elif images:

            await message.reply_photo(
                photo=images[0],
                caption="𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳"
            )

        else:

            await message.reply_text(
                "No media found."
            )

    except Exception as e:

        await message.reply_text(
            f"Pinterest Error:\n{e}"
        )