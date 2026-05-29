import os
import yt_dlp
import ffmpeg


async def download_youtube(url: str, format: str) -> str:
    """Downloads a YouTube video or audio and returns the file path."""

    ydl_opts = {
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "cookiefile": "cookies.txt" if os.path.exists("cookies.txt") else None,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
    }

    if format == "audio":
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
            "format": (
                "bv*+ba/"
                "bestvideo+bestaudio/"
                "bestvideo[height<=1080]+bestaudio/"
                "best[height<=1080]/best"
            ),
            "merge_output_format": "mp4",
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)

    if format == "audio":
        mp3_path = os.path.splitext(file_path)[0] + ".mp3"
        if os.path.exists(mp3_path):
            return mp3_path
        return file_path

    if not os.path.exists(file_path):
        base = os.path.splitext(file_path)[0]
        for ext in ("mp4", "mkv", "webm"):
            candidate = f"{base}.{ext}"
            if os.path.exists(candidate):
                return candidate

    return file_path
