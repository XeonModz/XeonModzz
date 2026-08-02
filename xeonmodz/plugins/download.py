# Version: 1.2
# ©️ 2026 XeonModz ALL RIGHTS RESERVED

import time

import requests
from pyrogram import filters
from pyrogram.types import InputMediaPhoto, InputMediaVideo
from xeonmodz import app
from xeonmodz.lib.mode import isPrivate

API_BASE = "https://xeon-apis.onrender.com"
CAPTION = "𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳"

# Render free tier can cold-start (30-60s) after idling, and slow scrapes
# (Facebook especially) can take a while too — give requests plenty of
# room before giving up and calling it a failure.
REQUEST_TIMEOUT = 90

# If the very first request hits the API while it's still waking up from
# a cold start, it can come back with a malformed/incomplete response
# (including a stray 422). One quiet retry clears this up almost every
# time without the user ever noticing.
COLD_START_RETRIES = 1
COLD_START_RETRY_DELAY = 5  # seconds


def fetch_json(endpoint: str, params: dict):
    """
    GET a JSON endpoint with automatic query-param encoding (requests
    handles this for us — never hand-build the query string, since a
    raw Instagram/Facebook/Pinterest URL often contains its own '?' and
    '=' characters that would otherwise corrupt the outer query string).

    Retries once on timeout / bad-JSON / 4xx-5xx to smooth over Render
    cold starts. Returns (data, error_message). If error_message is not
    None, data should be ignored.
    """
    last_error = None

    for attempt in range(COLD_START_RETRIES + 1):
        try:
            r = requests.get(
                f"{API_BASE}/{endpoint}",
                params=params,
                timeout=REQUEST_TIMEOUT,
            )

            try:
                data = r.json()
            except ValueError:
                last_error = f"Bad response from API (HTTP {r.status_code})"
                if attempt < COLD_START_RETRIES:
                    time.sleep(COLD_START_RETRY_DELAY)
                    continue
                return None, last_error

            if r.status_code >= 400:
                last_error = (
                    data.get("error_message")
                    or data.get("error")
                    or data.get("message")
                    or f"API returned HTTP {r.status_code}"
                )
                if attempt < COLD_START_RETRIES:
                    time.sleep(COLD_START_RETRY_DELAY)
                    continue
                return None, last_error

            return data, None

        except requests.exceptions.Timeout:
            last_error = "Request timed out. Try again in a moment."
            if attempt < COLD_START_RETRIES:
                time.sleep(COLD_START_RETRY_DELAY)
                continue
            return None, last_error

        except requests.exceptions.RequestException as e:
            last_error = str(e)
            if attempt < COLD_START_RETRIES:
                time.sleep(COLD_START_RETRY_DELAY)
                continue
            return None, last_error

    return None, last_error


@app.on_message(filters.command("insta"))
@isPrivate
async def instagram_downloader(_, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/insta <instagram_url>"
        )

    await message.react("⚡")

    data, error = fetch_json("insta", {"url": message.command[1]})

    if error:
        await message.react("💔")
        return await message.reply_text(f"Instagram Error:\n{error}")

    if not (data.get("success") or data.get("status")):
        await message.react("💔")
        return await message.reply_text(
            data.get("error", "Failed to fetch Instagram media.")
        )

    media_items = data.get("media") or []

    if not media_items:
        await message.react("💔")
        return await message.reply_text("No media found.")

    post_caption = data.get("caption") or ""
    caption = f"{post_caption}\n\n{CAPTION}" if post_caption else CAPTION

    try:
        # Single media item (post, reel, or single-image)
        if len(media_items) == 1:
            item = media_items[0]
            media_url = item.get("url")

            if not media_url:
                await message.react("💔")
                return await message.reply_text("No media found.")

            if item.get("type") == "video":
                await message.reply_video(media_url, caption=caption)
            else:
                await message.reply_photo(media_url, caption=caption)

        # Carousel (multiple images/videos) -> send as an album
        else:
            album = []

            for idx, item in enumerate(media_items):
                media_url = item.get("url")
                if not media_url:
                    continue

                cap = caption if idx == 0 else None

                if item.get("type") == "video":
                    album.append(InputMediaVideo(media_url, caption=cap))
                else:
                    album.append(InputMediaPhoto(media_url, caption=cap))

            if not album:
                await message.react("💔")
                return await message.reply_text("No media found.")

            await message.reply_media_group(album)

        await message.react("❤️")

    except Exception as e:
        await message.react("💔")
        await message.reply_text(f"Instagram Error:\n{e}")


@app.on_message(filters.command("pin"))
@isPrivate
async def pinterest_downloader(_, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/pin <pinterest_url>"
        )

    await message.react("⚡")

    data, error = fetch_json("pin", {"url": message.command[1]})

    if error:
        await message.react("💔")
        return await message.reply_text(f"Pinterest Error:\n{error}")

    if not (data.get("success") or data.get("status")):
        await message.react("💔")
        return await message.reply_text("Failed to fetch Pinterest media.")

    videos = data.get("videos") or []
    images = data.get("images") or []

    try:
        if videos:
            await message.reply_video(videos[0], caption=CAPTION)
        elif images:
            await message.reply_photo(images[0], caption=CAPTION)
        else:
            await message.react("💔")
            return await message.reply_text("No media found.")

        await message.react("❤️")

    except Exception as e:
        await message.react("💔")
        await message.reply_text(f"Pinterest Error:\n{e}")


@app.on_message(filters.command("fb"))
@isPrivate
async def facebook_downloader(_, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/fb <facebook_url>"
        )

    await message.react("⚡")

    data, error = fetch_json("fb", {"url": message.command[1]})

    if error:
        await message.react("💔")
        return await message.reply_text(f"Facebook Error:\n{error}")

    if not (data.get("success") or data.get("status")):
        await message.react("💔")
        return await message.reply_text(
            data.get("message", "Failed to fetch Facebook video.")
        )

    title = data.get("title") or ""
    caption = f"{title}\n\n{CAPTION}" if title else CAPTION

    videos = data.get("videos") or {}
    video_url = (videos.get("hd") or {}).get("url") or (videos.get("sd") or {}).get("url")

    if not video_url:
        await message.react("💔")
        return await message.reply_text("No video found.")

    try:
        await message.reply_video(video_url, caption=caption)
        await message.react("❤️")

    except Exception as e:
        await message.react("💔")
        await message.reply_text(f"Facebook Error:\n{e}")
