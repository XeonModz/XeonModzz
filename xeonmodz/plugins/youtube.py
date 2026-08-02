# # Version: 1.0 Beta
# # ©️ 2026 XeonModz ALL RIGHTS RESERVED

# import os
# import requests
# import asyncio
# from pyrogram import filters
# from pyrogram.types import Message
# from xeonmodz import app
# from xeonmodz.lib.mode import isPrivate
# from xeonmodz.lib.mongo import save_yt_cookies, get_yt_cookies
# from xeonmodz.lib.youtube import download_youtube
# import config

# API = "https://xeon-yt-api.onrender.com"

# # Restore cookies.txt from MongoDB or config on startup
# try:
#     cookies_data = get_yt_cookies()
#     if not cookies_data and hasattr(config, "COOKIES") and config.COOKIES:
#         cookies_data = config.COOKIES
#     if cookies_data:
#         with open("cookies.txt", "w", encoding="utf-8") as f:
#             f.write(cookies_data)
#         print("YouTube cookies loaded successfully.")
# except Exception as e:
#     print(f"Error loading YouTube cookies: {e}")


# @app.on_message(filters.command("setytcookies") & filters.reply & filters.user(config.SUDO))
# async def set_yt_cookies(client, message):
#     replied = message.reply_to_message

#     if not replied or not replied.document:
#         return await message.reply("❌ Please reply to a .txt file.")

#     file_name = replied.document.file_name

#     if not file_name.endswith(".txt"):
#         return await message.reply("❌ The file must be a .txt file.")

#     try:
#         download_path = "cookies.txt"
#         await client.download_media(replied, file_name=download_path)
#         with open(download_path, "r", encoding="utf-8") as f:
#             cookies_data = f.read()
#         save_yt_cookies(cookies_data)
#         await message.reply("✅ Saved as cookies.txt and uploaded to MongoDB.")
#     except Exception as e:
#         await message.reply(f"❌ Failed to save file:\n`{e}`")


# @app.on_message(filters.command("audio"))
# @isPrivate
# async def yt_audio_handler(client, message: Message):
#     query = (
#         message.reply_to_message.text
#         if message.reply_to_message and message.reply_to_message.text
#         else message.text.split(maxsplit=1)[1]
#         if len(message.command) > 1
#         else None
#     )
#     if not query:
#         return await message.reply("❌ Please reply to a YouTube link or type `/audio <url|name>`.")

#     try:
#         await message.react("🦄")
#         url = query if query.startswith("http") else f"ytsearch:{query}"
#         file_path = await download_youtube(url, "audio")
        
#         if not file_path or not os.path.exists(file_path):
#             await message.react("❌")
#             return

#         title = os.path.splitext(os.path.basename(file_path))[0]
        
#         await client.send_audio(
#             chat_id=message.chat.id,
#             audio=file_path,
#             title=title,
#             performer="YouTube",
#             caption=f"🎧 **{title}**",
#         )
#         try:
#             os.remove(file_path)
#         except Exception:
#             pass
#         await message.react("❤️")
#     except Exception:
#         await message.react("❌")


# @app.on_message(filters.command("video"))
# @isPrivate
# async def yt_video_handler(client, message: Message):
#     query = (
#         message.reply_to_message.text
#         if message.reply_to_message and message.reply_to_message.text
#         else message.text.split(maxsplit=1)[1]
#         if len(message.command) > 1
#         else None
#     )
#     if not query:
#         return await message.reply("❌ Please reply to a YouTube link or type `/video <url|name>`.")

#     try:
#         await message.react("🦄")
#         url = query if query.startswith("http") else f"ytsearch:{query}"
#         file_path = await download_youtube(url, "video")
        
#         if not file_path or not os.path.exists(file_path):
#             await message.react("❌")
#             return

#         title = os.path.splitext(os.path.basename(file_path))[0]
        
#         await client.send_video(
#             chat_id=message.chat.id,
#             video=file_path,
#             caption=f"🎬 **{title}**",
#             supports_streaming=True
#         )
#         try:
#             os.remove(file_path)
#         except Exception:
#             pass
#         await message.react("❤️")
#     except Exception:
#         await message.react("❌")


# @app.on_message(filters.command(["song"]))
# async def ytmp3_handler(client, message):
#     if len(message.command) < 2 and not message.reply_to_message:
#         return await message.reply("❌ Please reply to a YouTube link or type `/song <url>`.")

#     query = (
#         message.reply_to_message.text
#         if message.reply_to_message and message.reply_to_message.text
#         else message.text.split(maxsplit=1)[1]
#         if len(message.command) > 1
#         else None
#     )

#     try:
#         await message.react("🦄")
#         api_success = False

#         if query.startswith("http"):
#             try:
#                 data = requests.get(
#                     f"{API}/ytmp3",
#                     params={"url": query},
#                     timeout=30
#                 ).json()

#                 if data.get("status"):
#                     await client.send_audio(
#                         chat_id=message.chat.id,
#                         audio=data["download"],
#                         title=data.get("title", "HQ Audio"),
#                         performer="Xeon Vro HQ",
#                         file_name=f"{data.get('title', 'audio')}.mp3"
#                     )
#                     api_success = True
#             except Exception:
#                 pass

#         if not api_success:
#             # Fallback to local yt-dlp download
#             url = query if query.startswith("http") else f"ytsearch:{query}"
#             file_path = await download_youtube(url, "audio")
#             if file_path and os.path.exists(file_path):
#                 title = os.path.splitext(os.path.basename(file_path))[0]
#                 await client.send_audio(
#                     chat_id=message.chat.id,
#                     audio=file_path,
#                     title=title,
#                     performer="YouTube",
#                     caption=f"🎧 **{title}**",
#                 )
#                 try:
#                     os.remove(file_path)
#                 except Exception:
#                     pass
#                 api_success = True

#         if api_success:
#             await message.react("❤️")
#         else:
#             await message.react("❌")

#     except Exception:
#         await message.react("❌")

# Version: 1.0
# ©️ 2026 XeonModz ALL RIGHTS RESERVED

import re
import time

import requests
from pyrogram import filters
from xeonmodz import app
from xeonmodz.lib.mode import isPrivate

CAPTION = "𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳"
YTMP4_URL = "https://ht.flvto.online/converter"
YTMP4_HEADERS = {"origin": "https://ht.flvto.online"}
YT_ID_RE = re.compile(r"(?:youtube\.com/(?:watch\?v=|shorts/)|youtu\.be/)([\w-]{11})")


def get_download(video_id, file_type="mp3"):
    for _ in range(12):
        r = requests.post(YTMP4_URL, headers=YTMP4_HEADERS,
                           json={"id": video_id, "fileType": file_type}, timeout=30)
        data = r.json()
        if data.get("status") in ("ok", "success"):
            link = data.get("link") or data.get("url")

            if not link:
                # mp4 responses come back as a list of formats (yt-dlp style)
                # instead of a single top-level link. Pick the best one that
                # actually has audio — some formats are video-only.
                formats = data.get("formats") or []
                playable = [f for f in formats if f.get("audioQuality") and f.get("url")]
                pool = playable or formats
                if pool:
                    best = max(pool, key=lambda f: f.get("bitrate") or 0)
                    link = best.get("url")

            return data.get("title") or "YouTube", link, data
        if data.get("status") == "error":
            raise RuntimeError(data.get("message", "Conversion failed"))
        time.sleep(5)
    raise RuntimeError("Timeout")


async def handle_yt(message, file_type):
    if len(message.command) < 2:
        return await message.reply_text(f"Usage:\n/{message.command[0]} <youtube_url>")

    match = YT_ID_RE.search(message.command[1])
    if not match:
        return await message.reply_text("Invalid YouTube link.")

    await message.react("⚡")
    try:
        title, url, _ = get_download(match.group(1), file_type)
        if not url:
            raise RuntimeError("No media found.")

        caption = f"{title}\n\n{CAPTION}" if len(title) < 950 else CAPTION

        if file_type == "mp3":
            await message.reply_audio(url, caption=caption, title=title)
        else:
            await message.reply_video(url, caption=caption)

        await message.react("❤️")

    except Exception as e:
        await message.react("💔")
        await message.reply_text(f"YouTube Error:\n{e}")


@app.on_message(filters.command("song"))
@isPrivate
async def song_downloader(_, message):
    await handle_yt(message, "mp3")


@app.on_message(filters.command("video"))
@isPrivate
async def video_downloader(_, message):
    await handle_yt(message, "mp4")
