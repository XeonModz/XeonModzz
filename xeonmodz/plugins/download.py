# Version: 1.1
# ©️ 2026 XeonModz ALL RIGHTS RESERVED

from pyrogram import filters
from pyrogram.types import InputMediaPhoto, InputMediaVideo
from xeonmodz import app
from xeonmodz.lib.mode import isPrivate
import requests

API_BASE = "https://xeon-apis.onrender.com"
CAPTION = "𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳"

# Render free tier can cold-start (30-60s) after idling, and slow Facebook
# scrapes can take a while too — give requests plenty of room before
# giving up and calling it a failure.
REQUEST_TIMEOUT = 90


@app.on_message(filters.command("insta"))
@isPrivate
async def instagram_downloader(_, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/insta <instagram_url>"
        )

    await message.react("⚡")

    try:
        r = requests.get(
            f"{API_BASE}/insta",
            params={"url": message.command[1]},
            timeout=REQUEST_TIMEOUT
        )

        try:
            data = r.json()
        except ValueError:
            await message.react("💔")
            return await message.reply_text(
                f"Instagram Error:\nBad response from API (HTTP {r.status_code})"
            )

        if not (data.get("success") or data.get("status")):
            await message.react("💔")
            return await message.reply_text(
                data.get(
                    "error",
                    "Failed to fetch Instagram media."
                )
            )

        media_items = data.get("media", [])

        if not media_items:
            await message.react("💔")
            return await message.reply_text(
                "No media found."
            )

        post_caption = data.get("caption") or ""
        caption = f"{post_caption}\n\n{CAPTION}" if post_caption else CAPTION

        # Single media item (post, reel, or single-image)
        if len(media_items) == 1:
            item = media_items[0]

            if item.get("type") == "video":
                await message.reply_video(
                    item.get("url"),
                    caption=caption
                )
            else:
                await message.reply_photo(
                    item.get("url"),
                    caption=caption
                )

        # Carousel (multiple images/videos) -> send as an album
        else:
            album = []

            for idx, item in enumerate(media_items):
                cap = caption if idx == 0 else None

                if item.get("type") == "video":
                    album.append(
                        InputMediaVideo(
                            item.get("url"),
                            caption=cap
                        )
                    )
                else:
                    album.append(
                        InputMediaPhoto(
                            item.get("url"),
                            caption=cap
                        )
                    )

            await message.reply_media_group(album)

        await message.react("❤️")

    except requests.exceptions.Timeout:
        await message.react("💔")
        await message.reply_text(
            "Instagram Error:\nRequest timed out. Try again in a moment."
        )

    except Exception as e:
        await message.react("💔")
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

    await message.react("⚡")

    try:
        r = requests.get(
            f"{API_BASE}/pin",
            params={"url": message.command[1]},
            timeout=REQUEST_TIMEOUT
        )

        try:
            data = r.json()
        except ValueError:
            await message.react("💔")
            return await message.reply_text(
                f"Pinterest Error:\nBad response from API (HTTP {r.status_code})"
            )

        if not (data.get("success") or data.get("status")):
            await message.react("💔")
            return await message.reply_text(
                "Failed to fetch Pinterest media."
            )

        videos = data.get("videos", [])
        images = data.get("images", [])

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
            await message.react("💔")
            return await message.reply_text(
                "No media found."
            )

        await message.react("❤️")

    except requests.exceptions.Timeout:
        await message.react("💔")
        await message.reply_text(
            "Pinterest Error:\nRequest timed out. Try again in a moment."
        )

    except Exception as e:
        await message.react("💔")
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

    await message.react("⚡")

    try:
        r = requests.get(
            f"{API_BASE}/fb",
            params={"url": message.command[1]},
            timeout=REQUEST_TIMEOUT
        )

        try:
            data = r.json()
        except ValueError:
            await message.react("💔")
            return await message.reply_text(
                f"Facebook Error:\nBad response from API (HTTP {r.status_code})"
            )

        if not (data.get("success") or data.get("status")):
            await message.react("💔")
            return await message.reply_text(
                data.get(
                    "message",
                    "Failed to fetch Facebook video."
                )
            )

        title = data.get("title") or ""
        caption = f"{title}\n\n{CAPTION}" if title else CAPTION

        videos = data.get("videos") or {}

        video_url = (videos.get("hd") or {}).get("url")

        if not video_url:
            video_url = (videos.get("sd") or {}).get("url")

        if not video_url:
            await message.react("💔")
            return await message.reply_text(
                "No video found."
            )

        await message.reply_video(
            video_url,
            caption=caption
        )

        await message.react("❤️")

    except requests.exceptions.Timeout:
        await message.react("💔")
        await message.reply_text(
            "Facebook Error:\nRequest timed out. Try again in a moment."
        )

    except Exception as e:
        await message.react("💔")
        await message.reply_text(
            f"Facebook Error:\n{e}"
        )
