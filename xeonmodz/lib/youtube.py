# Version: 1.0 Beta
# ©️ 2026 XeonModz ALL RIGHTS RESERVED

import os
import yt_dlp
import shutil
import glob
import asyncio

DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


def download_youtube_sync(url: str, format_type: str) -> str:
    """Downloads a YouTube video or audio synchronously and returns the file path.
    This should be run in an executor to avoid blocking the asyncio event loop.
    """
    ffmpeg_available = shutil.which("ffmpeg") is not None
    cookie_file = "cookies.txt" if os.path.exists("cookies.txt") else None

    ydl_opts = {
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "cookiefile": cookie_file,
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        },
    }

    if format_type == "audio":
        if ffmpeg_available:
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            })
        else:
            ydl_opts.update({
                "format": "bestaudio/best",
            })
    else:
        # Video format configuration
        if ffmpeg_available:
            ydl_opts.update({
                "format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
                "merge_output_format": "mp4",
            })
        else:
            ydl_opts.update({
                "format": "best[height<=1080][ext=mp4]/best[height<=1080]/best",
            })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)

    # Handle postprocessors modifying file extension
    if not os.path.exists(file_path):
        base, _ = os.path.splitext(file_path)
        if format_type == "audio":
            if os.path.exists(base + ".mp3"):
                return base + ".mp3"
            for ext in [".m4a", ".webm", ".opus", ".aac"]:
                if os.path.exists(base + ext):
                    return base + ext
        else:
            for ext in [".mp4", ".mkv", ".webm", ".3gp"]:
                if os.path.exists(base + ext):
                    return base + ext
        matches = glob.glob(glob.escape(base) + ".*")
        if matches:
            return matches[0]

    return file_path


async def download_youtube(url: str, format_type: str) -> str:
    """Async wrapper to run the synchronous download_youtube_sync in an executor."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, download_youtube_sync, url, format_type)

