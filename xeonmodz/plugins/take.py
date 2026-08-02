# Version: 1.0
# ©️ 2026 XeonModz ALL RIGHTS RESERVED

import asyncio
import os
import time

import requests
from pyrogram import filters
from xeonmodz import app
from xeonmodz.lib.mode import isPrivate

CAPTION = "𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳"
DOWNLOAD_DIR = "downloads"
DEFAULT_TITLE = "𝚾𝛆𝛐𝛈"
DEFAULT_ARTIST = "𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳"
DEFAULT_THUMB = "https://i.ibb.co/wHnkzmd/temp.jpg"


@app.on_message(filters.command("take"))
@isPrivate
async def set_audio_tags(_, message):
    reply = message.reply_to_message

    has_audio = reply and (
        reply.audio or reply.voice
        or (reply.document and (reply.document.mime_type or "").startswith("audio/"))
    )

    if not has_audio:
        return await message.reply_text(
            "Reply to an audio with:\n/take title;artist;imageUrl"
        )

    if len(message.command) < 2:
        title, artist, image_url = DEFAULT_TITLE, DEFAULT_ARTIST, DEFAULT_THUMB
    else:
        parts = [p.strip() for p in message.text.split(None, 1)[1].split(";")]
        title = parts[0] if parts and parts[0] else DEFAULT_TITLE
        artist = parts[1] if len(parts) > 1 and parts[1] else DEFAULT_ARTIST
        image_url = parts[2] if len(parts) > 2 and parts[2] else DEFAULT_THUMB

    await message.react("⚡")
    status = await message.reply_text("Updating tags…")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    stamp = int(time.time())
    in_path = os.path.join(DOWNLOAD_DIR, f"{stamp}_in")
    cover_path = os.path.join(DOWNLOAD_DIR, f"{stamp}_cover.jpg")
    out_path = os.path.join(DOWNLOAD_DIR, f"{stamp}_out.mp3")

    try:
        in_path = await reply.download(file_name=in_path)

        r = requests.get(image_url, timeout=30)
        r.raise_for_status()
        with open(cover_path, "wb") as f:
            f.write(r.content)

        # Re-encode audio (rather than -c:a copy) so this works regardless
        # of the source format — voice notes are opus/ogg, not mp3.
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg", "-y",
            "-i", in_path, "-i", cover_path,
            "-map", "0:a", "-map", "1:0",
            "-c:a", "libmp3lame", "-q:a", "2",
            "-c:v", "mjpeg", "-disposition:v", "attached_pic",
            "-id3v2_version", "3",
            "-metadata", f"title={title}",
            "-metadata", f"artist={artist}",
            out_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await proc.communicate()

        if proc.returncode != 0 or not os.path.exists(out_path):
            raise RuntimeError(stderr.decode(errors="ignore")[-300:] or "ffmpeg failed")

        await message.reply_audio(
            out_path, title=title, performer=artist, thumb=cover_path, caption=CAPTION
        )
        await message.react("❤️")

    except Exception as e:
        await message.react("💔")
        await message.reply_text(f"Tag Error:\n{e}")

    finally:
        await status.delete()
        for path in (in_path, cover_path, out_path):
            if path and os.path.exists(path):
                os.remove(path)
