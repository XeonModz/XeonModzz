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
    except:
        pass

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/insta instagram_url"
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
            f"Error:\n{e}"
        )


# Pinterest Downloader
@app.on_message(filters.command("pin"))
@isPrivate
async def pinterest_downloader(client, message):

    try:
        await message.react("⚡")
    except:
        pass

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/pin pinterest_url"
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

    videos = [
        vid for vid in data.get("videos", [])
        if isinstance(vid, str)
        and vid.startswith("http")
    ]

    for vid in videos:

        try:
            await message.reply_video(
                video=vid,
                caption="𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳"
            )
        except Exception:
            pass

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
                caption="𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳"
            )
        except Exception:
            pass

    if not videos and not images:
        await message.reply_text(
            "No media found."
        )