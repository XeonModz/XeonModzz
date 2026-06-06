# import os
# import uuid
# import shutil
# import subprocess
# from pyrogram import Client, filters
# from pyrogram.types import Message
# from yt_dlp import YoutubeDL
# from xeonmodz import app
# from xeonmodz.lib.mode import isPrivate
# from xeonmodz.lib.mongo import save_yt_cookies, get_yt_cookies
# import config
# DOWNLOAD_FOLDER = "downloads"
# if not os.path.exists(DOWNLOAD_FOLDER):
#     os.makedirs(DOWNLOAD_FOLDER)

# # Restore cookies.txt from MongoDB on startup
# cookies_data = get_yt_cookies()
# if cookies_data:
#     with open(os.path.join(os.getcwd(), "cookies.txt"), "w", encoding="utf-8") as f:
#         f.write(cookies_data)

# @app.on_message(filters.command("setytcookies") & filters.reply & filters.user(config.SUDO))
# async def set_yt_cookies(client, message):
#     replied = message.reply_to_message

#     if not replied or not replied.document:
#         return await message.reply("❌ Please reply to a .txt file.")

#     file_name = replied.document.file_name

#     if not file_name.endswith(".txt"):
#         return await message.reply("❌ The file must be a .txt file.")

#     try:
#         download_path = os.path.join(os.getcwd(), "cookies.txt")
#         await client.download_media(replied, file_name=download_path)
#         with open(download_path, "r", encoding="utf-8") as f:
#             cookies_data = f.read()
#         save_yt_cookies(cookies_data)
#         await message.reply(f"✅ Saved as ytcookies.txt in:\n`{download_path}` and uploaded to MongoDB.")
#     except Exception as e:
#         await message.reply(f"❌ Failed to save file:\n`{e}`")

# @app.on_message(filters.command("audio"))
# @isPrivate
# async def yt_audio_handler(client, message: Message):
#     query = (
#         message.reply_to_message.text
#         if message.reply_to_message
#         else message.text.split(maxsplit=1)[1]
#         if len(message.command) > 1
#         else None
#     )
#     if not query:
#         return await message.reply("❌ Please reply to a YouTube link or type `/audio <url|name>`.")

#     search_query = f"ytsearch:{query}" if not query.startswith("http") else query

#     ydl_opts = {
#         'format': 'bestaudio[ext=mp3]/bestaudio/best',
#         'cookiefile': 'cookies.txt',
#         'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
#         'quiet': True,
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
#     }

#     try:
#         status = await message.reply("🔍 Downloading audio...")
#         with YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(search_query, download=True)
#             title = info.get('title', 'audio')
#             file_path = ydl.prepare_filename(info)
#             # Try to find a valid file with a known extension
#             if not os.path.exists(file_path):
#                 base, _ = os.path.splitext(file_path)
#                 found = False
#                 for ext in ['mp3', 'm4a', 'webm', 'opus']:
#                     alt_path = f"{base}.{ext}"
#                     if os.path.exists(alt_path):
#                         file_path = alt_path
#                         found = True
#                         break
#                 if not found:
#                     # Try to find any file with the same base name
#                     import glob
#                     matches = glob.glob(base + ".*")
#                     if matches:
#                         file_path = matches[0]
#                     else:
#                         raise FileNotFoundError(f"No downloaded file found for {base}")

#         # Check extension and convert to mp3 if possible
#         ext = os.path.splitext(file_path)[1].lower()
#         ffmpeg_installed = shutil.which("ffmpeg") is not None
#         output_path = file_path
#         if ext != ".mp3" and ffmpeg_installed:
#             output_path = os.path.splitext(file_path)[0] + ".mp3"
#             cmd = ["ffmpeg", "-y", "-i", file_path, output_path]
#             subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#             if os.path.exists(output_path):
#                 os.remove(file_path)
#             else:
#                 output_path = file_path  # fallback if conversion failed

#         await status.edit("📤 Uploading audio...")
#         with open(output_path, "rb") as audio_file:
#             await client.send_audio(
#                 chat_id=message.chat.id,
#                 audio=audio_file,
#                 title=title,
#                 performer="YouTube",
#                 caption=f"🎧 **{title}**",
#             )
#         os.remove(output_path)
#         await status.delete()
#     except Exception as e:
#         await message.reply(f"❌ Error: `{e}`")

# @app.on_message(filters.command("video"))
# @isPrivate
# async def yt_video_handler(client, message: Message):
#     query = (
#         message.reply_to_message.text
#         if message.reply_to_message
#         else message.text.split(maxsplit=1)[1]
#         if len(message.command) > 1
#         else None
#     )
#     if not query:
#         return await message.reply("❌ Please reply to a YouTube link or type `/video <url|name>`.")

#     search_query = f"ytsearch:{query}" if not query.startswith("http") else query

#     ydl_opts = {
#         'format': 'best[ext=mp4][height<=1080]/best[height<=1080]/best',
#         'cookiefile': 'cookies.txt',
#         'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
#         'quiet': True,
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
#     }

#     try:
#         status = await message.reply("🔍 Downloading video...")
#         with YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(search_query, download=True)
#             title = info.get('title', 'video')
#             file_path = ydl.prepare_filename(info)
#             # Find the actual downloaded file (could be mp4, webm, mkv, etc.)
#             if not os.path.exists(file_path):
#                 base, _ = os.path.splitext(file_path)
#                 for ext in ['mp4', 'webm', 'mkv']:
#                     alt_path = f"{base}.{ext}"
#                     if os.path.exists(alt_path):
#                         file_path = alt_path
#                         break

#         output_filename = f"{uuid.uuid4()}{os.path.splitext(file_path)[1]}"
#         output_path = os.path.join(DOWNLOAD_FOLDER, output_filename)
#         os.rename(file_path, output_path)

#         await status.edit("📤 Uploading video...")
#         with open(output_path, "rb") as video_file:
#             await client.send_video(
#                 chat_id=message.chat.id,
#                 video=video_file,
#                 caption=f"🎬 **{title}**",
#                 supports_streaming=True
#             )
#         os.remove(output_path)
#         await status.delete()
#     except Exception as e:
#         await message.reply(f"❌ Error: `{e}`")





import requests
from pyrogram import filters
from xeonmodz import app

API = "https://xeon-yt-api.onrender.com"


@app.on_message(filters.command(["song"]))
async def ytmp3_handler(client, message):
    if len(message.command) < 2:
        return

    try:
        url = message.command[1]

        await message.react("🦄")

        data = requests.get(
            f"{API}/ytmp3",
            params={"url": url},
            timeout=120
        ).json()

        if not data.get("status"):
            return await message.react("❌")

        await client.send_audio(
            chat_id=message.chat.id,
            audio=data["download"],
            title=data.get("title", "HQ Audio"),
            performer="Xeon Vro HQ",
            file_name=f"{data.get('title', 'audio')}.mp3"
        )

        await message.react("❤️")

    except Exception:
        await message.react("❌")