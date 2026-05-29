from pyrogram import filters
from xeonmodz.lib.mode import isPrivate
from xeonmodz import app
import requests


# Instagram Downloader
@app.on_message(filters.command("insta"))
@isPrivate
async def insta_downloader(client, message):

    try:
        await message.react("⚡")
    except Exception:
        pass

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/insta instagram_url"
        )

    query = message.command[1]

    try:
        response = requests.get(
            f"https://xeon-insta-api.onrender.com/insta?url={query}"
        )
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

    try:

        if media_type == "video":

            await message.reply_video(
                video=media,
                caption="𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳"
            )

        elif media_type == "image":

            await message.reply_photo(
                photo=media,
                caption="𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳"
            )

        else:

            await message.reply_text(
                "Unsupported media type."
            )

    except Exception as e:

        await message.reply_text(
            f"Instagram Error:\n{e}"
        )


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
            f"https://xeon-pin-api.onrender.com/pin?url={query}"
        )

        data = response.json()

    except Exception as e:

        return await message.reply_text(
            f"API Error:\n{e}"
        )

    if not data.get("status"):

        return await message.reply_text(
            "Failed to fetch Pinterest media."
        )

    video = data.get("video")
    image = data.get("image")

    try:

        if video:

            await message.reply_video(
                video=video,
                caption="𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳"
            )

        elif image:

            await message.reply_photo(
                photo=image,
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