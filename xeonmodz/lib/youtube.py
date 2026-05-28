import os
import yt_dlp
import ffmpeg


async def download_youtube(url: str, format: str) -> str:
    """Downloads a YouTube video or audio and returns the file path."""
    ydl_opts = {
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "format": "bestaudio/best" if format == "audio" else "bestvideo+bestaudio/best",
        "merge_output_format": "mp4" if format == "video" else "mp3",
        "postprocessors": [],
        "noplaylist": True,
        "quiet": True,
        "cookiefile": "cookies.txt" ,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
    
    if format == "audio":
        audio_path = file_path.rsplit(".", 1)[0] + ".mp3"
        ffmpeg.input(file_path).output(audio_path, format="mp3").run()
        os.remove(file_path)
        return audio_path
    
    return file_path