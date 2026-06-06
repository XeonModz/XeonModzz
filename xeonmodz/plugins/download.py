# from pyrogram import filters
# from xeonmodz import app
# from xeonmodz.lib.mode import isPrivate
# import requests

# API_BASE = "https://xeon-apis.onrender.com"

# CAPTION = "𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳"


# @app.on_message(filters.command("insta"))
# @isPrivate
# async def instagram_downloader(_, message):

#     if len(message.command) < 2:
#         return await message.reply_text(
#             "Usage:\n/insta <instagram_url>"
#         )

#     try:
#         r = requests.get(
#             f"{API_BASE}/insta",
#             params={"url": message.command[1]},
#             timeout=30
#         )

#         data = r.json()

#         if not (data.get("success") or data.get("status")):
#             return await message.reply_text(
#                 data.get("error", "Failed to fetch Instagram media.")
#             )

#         media = data.get("media")

#         if data.get("type") == "video":
#             await message.reply_video(
#                 media,
#                 caption=CAPTION
#             )
#         else:
#             await message.reply_photo(
#                 media,
#                 caption=CAPTION
#             )

#     except Exception as e:
#         await message.reply_text(f"Instagram Error:\n{e}")


# @app.on_message(filters.command("pin"))
# @isPrivate
# async def pinterest_downloader(_, message):

#     if len(message.command) < 2:
#         return await message.reply_text(
#             "Usage:\n/pin <pinterest_url>"
#         )

#     try:
#         r = requests.get(
#             f"{API_BASE}/pin",
#             params={"url": message.command[1]},
#             timeout=30
#         )

#         data = r.json()

#         if not (data.get("success") or data.get("status")):
#             return await message.reply_text(
#                 "Failed to fetch Pinterest media."
#             )

#         videos = data.get("videos", [])
#         images = data.get("images", [])

#         if videos:
#             await message.reply_video(
#                 videos[0],
#                 caption=CAPTION
#             )
#         elif images:
#             await message.reply_photo(
#                 images[0],
#                 caption=CAPTION
#             )
#         else:
#             await message.reply_text("No media found.")

#     except Exception as e:
#         await message.reply_text(f"Pinterest Error:\n{e}")


# @app.on_message(filters.command("fb"))
# @isPrivate
# async def facebook_downloader(_, message):

#     if len(message.command) < 2:
#         return await message.reply_text(
#             "Usage:\n/fb <facebook_url>"
#         )

#     try:
#         r = requests.get(
#             f"{API_BASE}/fb",
#             params={"url": message.command[1]},
#             timeout=60
#         )

#         data = r.json()

#         if not (data.get("success") or data.get("status")):
#             return await message.reply_text(
#                 "Failed to fetch Facebook video."
#             )

#         video_url = (
#             data.get("videos", {})
#             .get("hd", {})
#             .get("url")
#         )

#         if not video_url:
#             video_url = (
#                 data.get("videos", {})
#                 .get("sd", {})
#                 .get("url")
#             )

#         if not video_url:
#             return await message.reply_text(
#                 "No video found."
#             )

#         await message.reply_video(
#             video_url,
#             caption=CAPTION
#         )

#     except Exception as e:
#         await message.reply_text(f"Facebook Error:\n{e}")





from pyrogram import filters
from xeonmodz import app
from xeonmodz.lib.mode import isPrivate

import asyncio
import requests

API_BASE = "https://xeon-apis.onrender.com"
CAPTION = "𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳"


async def react(message, emoji):
    try:
        await message.react(emoji)
    except Exception:
        pass


async def fetch_json(endpoint, url):
    def req():
        return requests.get(
            f"{API_BASE}/{endpoint}",
            params={"url": url},
            timeout=60
        ).json()

    return await asyncio.to_thread(req)


@app.on_message(filters.command("insta"))
@isPrivate
async def instagram_downloader(_, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/insta <instagram_url>"
        )

    await react(message, "⏳")

    try:
        data = await fetch_json(
            "insta",
            message.command[1]
        )

        if not (data.get("success") or data.get("status")):
            await react(message, "❌")
            return await message.reply_text(
                data.get(
                    "error",
                    "Failed to fetch Instagram media."
                )
            )

        media = data.get("media")

        await react(message, "📤")

        if data.get("type") == "video":
            await message.reply_video(
                media,
                caption=CAPTION
            )
        else:
            await message.reply_photo(
                media,
                caption=CAPTION
            )

        await react(message, "✅")

    except Exception as e:
        await react(message, "❌")
        await message.reply_text(
            f"Instagram Error:\n{e}"
        )


@app.on_message(filters.command("pin"))
@isPrivate
async def pinterest_downloader(_, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/pin <pinterest_url>"
        )

    await react(message, "⏳")

    try:
        data = await fetch_json(
            "pin",
            message.command[1]
        )

        if not (data.get("success") or data.get("status")):
            await react(message, "❌")
            return await message.reply_text(
                "Failed to fetch Pinterest media."
            )

        videos = data.get("videos", [])
        images = data.get("images", [])

        await react(message, "📤")

        if videos:
            await message.reply_video(
                videos[0],
                caption=CAPTION
            )

        elif images:
            await message.reply_photo(
                images[0],
                caption=CAPTION
            )

        else:
            await react(message, "❌")
            return await message.reply_text(
                "No media found."
            )

        await react(message, "✅")

    except Exception as e:
        await react(message, "❌")
        await message.reply_text(
            f"Pinterest Error:\n{e}"
        )


@app.on_message(filters.command("fb"))
@isPrivate
async def facebook_downloader(_, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/fb <facebook_url>"
        )

    await react(message, "⏳")

    try:
        data = await fetch_json(
            "fb",
            message.command[1]
        )

        if not (data.get("success") or data.get("status")):
            await react(message, "❌")
            return await message.reply_text(
                "Failed to fetch Facebook video."
            )

        video_url = (
            data.get("videos", {})
            .get("hd", {})
            .get("url")
        ) or (
            data.get("videos", {})
            .get("sd", {})
            .get("url")
        )

        if not video_url:
            await react(message, "❌")
            return await message.reply_text(
                "No video found."
            )

        await react(message, "📤")

        await message.reply_video(
            video_url,
            caption=CAPTION
        )

        await react(message, "✅")

    except Exception as e:
        await react(message, "❌")
        await message.reply_text(
            f"Facebook Error:\n{e}"
        )