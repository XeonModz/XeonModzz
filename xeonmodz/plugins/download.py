# from pyrogram import filters
# from xeonmodz.lib.mode import isPrivate
# from xeonmodz import app
# import requests


# # Instagram Downloader
# # Pinterest Downloader
# @app.on_message(filters.command("pin"))
# @isPrivate
# async def pinterest_downloader(client, message):

#     try:
#         await message.react("⚡")
#     except Exception:
#         pass

#     if len(message.command) < 2:
#         return await message.reply_text(
#             "Usage:\n/pin pinterest_url"
#         )

#     query = message.command[1]

#     try:

#         response = requests.get(
#             f"https://xeon-pin-api.onrender.com/pin?url={query}",
#             timeout=30
#         )

#         data = response.json()

#     except Exception as e:

#         return await message.reply_text(
#             f"API Error:\n{e}"
#         )

#     if not data.get("success"):

#         return await message.reply_text(
#             "Failed to fetch Pinterest media."
#         )

#     videos = data.get("videos", [])
#     images = data.get("images", [])

#     try:

#         if videos:

#             await message.reply_video(
#                 video=videos[0],
#                 caption="𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳"
#             )

#         elif images:

#             await message.reply_photo(
#                 photo=images[0],
#                 caption="𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳"
#             )

#         else:

#             await message.reply_text(
#                 "No media found."
#             )

#     except Exception as e:

#         await message.reply_text(
#             f"Pinterest Error:\n{e}"
#         )






from pyrogram import filters
from xeonmodz import app
from xeonmodz.lib.mode import isPrivate
import requests

API_BASE = "https://xeon-pin-api.onrender.com"

CAPTION = "𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳"


# =========================
# INSTAGRAM
# =========================

@app.on_message(filters.command("insta"))
@isPrivate
async def instagram_downloader(_, message):

    try:
        await message.react("⚡")
    except:
        pass

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/insta <instagram_url>"
        )

    url = message.command[1]

    try:
        r = requests.get(
            f"{API_BASE}/insta",
            params={"url": url},
            timeout=30
        )

        data = r.json()

        if not data.get("success"):
            return await message.reply_text(
                data.get("error", "Failed to fetch Instagram media.")
            )

        media = data.get("media")
        media_type = data.get("type")

        if not media:
            return await message.reply_text(
                "No media found."
            )

        if media_type == "video":
            await message.reply_video(
                video=media,
                caption=CAPTION
            )
        else:
            await message.reply_photo(
                photo=media,
                caption=CAPTION
            )

    except Exception as e:
        await message.reply_text(
            f"Instagram Error:\n{e}"
        )


# =========================
# PINTEREST
# =========================

@app.on_message(filters.command("pin"))
@isPrivate
async def pinterest_downloader(_, message):

    try:
        await message.react("⚡")
    except:
        pass

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/pin <pinterest_url>"
        )

    url = message.command[1]

    try:
        r = requests.get(
            f"{API_BASE}/pin",
            params={"url": url},
            timeout=30
        )

        data = r.json()

        if not data.get("success"):
            return await message.reply_text(
                "Failed to fetch Pinterest media."
            )

        videos = data.get("videos", [])
        images = data.get("images", [])

        if videos:
            await message.reply_video(
                video=videos[0],
                caption=CAPTION
            )

        elif images:
            await message.reply_photo(
                photo=images[0],
                caption=CAPTION
            )

        else:
            await message.reply_text(
                "No media found."
            )

    except Exception as e:
        await message.reply_text(
            f"Pinterest Error:\n{e}"
        )


# =========================
# FACEBOOK
# =========================

@app.on_message(filters.command("fb"))
@isPrivate
async def facebook_downloader(_, message):

    try:
        await message.react("⚡")
    except:
        pass

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/fb <facebook_url>"
        )

    url = message.command[1]

    try:
        r = requests.get(
            f"{API_BASE}/fb",
            params={"url": url},
            timeout=60
        )

        data = r.json()

        if not data.get("success"):
            return await message.reply_text(
                "Failed to fetch Facebook video."
            )

        video_url = (
            data.get("videos", {})
            .get("hd", {})
            .get("url")
        )

        if not video_url:
            video_url = (
                data.get("videos", {})
                .get("sd", {})
                .get("url")
            )

        if not video_url:
            return await message.reply_text(
                "No video found."
            )

        await message.reply_video(
            video=video_url,
            caption=CAPTION
        )

    except Exception as e:
        await message.reply_text(
            f"Facebook Error:\n{e}"
        )