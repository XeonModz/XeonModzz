# Version: 1.0
# ©️ 2026 XeonModz ALL RIGHTS RESERVED

import asyncio
import os
import time

from pyrogram import filters
from xeonmodz import app
from xeonmodz.lib.mode import isPrivate

CAPTION = "𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳"
DOWNLOAD_DIR = "downloads"


@app.on_message(filters.command("mp3"))
@isPrivate
async def video_to_mp3(_, message):
    reply = message.reply_to_message

    has_video = reply and (
        reply.video or reply.animation
        or (reply.document and (reply.document.mime_type or "").startswith("video/"))
    )

    if not has_video:
        return await message.reply_text("Reply to a video with /mp3 to extract the audio.")

    await message.react("⚡️")
    status = await message.reply_text("Converting…")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    stamp = int(time.time())
    in_path = os.path.join(DOWNLOAD_DIR, f"{stamp}_in")
    out_path = os.path.join(DOWNLOAD_DIR, f"{stamp}_out.mp3")

    try:
        in_path = await reply.download(file_name=in_path)

        proc = await asyncio.create_subprocess_exec(
            "ffmpeg", "-y", "-i", in_path,
            "-vn", "-acodec", "libmp3lame", "-q:a", "2",
            out_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await proc.communicate()

        if proc.returncode != 0 or not os.path.exists(out_path):
            raise RuntimeError(stderr.decode(errors="ignore")[-300:] or "ffmpeg failed")

        title = (
            getattr(reply.video, "file_name", None)
            or getattr(reply.document, "file_name", None)
            or "Audio"
        )
        title = os.path.splitext(title)[0]

        await message.reply_audio(out_path, title=title, caption=CAPTION)
        await message.react("❤️")

    except Exception as e:
        await message.react("💔")
        await message.reply_text(f"Conversion Error:\n{e}")

    finally:
        await status.delete()
        for path in (in_path, out_path):
            if path and os.path.exists(path):
                os.remove(path)
