from pyrogram import filters
from xeonmodz import app
from xeonmodz.lib.mode import isPrivate
from config import FB_API
import requests


@app.on_message(filters.command("fb"))
@isPrivate
async def facebook_dl(_, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/fb <facebook_url>"
        )

    fb_url = message.command[1]

    msg = await message.reply_text("⏳ Fetching Facebook video...")

    try:
        r = requests.get(
            FB_API,
            params={"url": fb_url},
            timeout=60
        )

        if r.status_code != 200:
            return await msg.edit_text(
                f"❌ API Error\nHTTP {r.status_code}"
            )

        try:
            data = r.json()
        except Exception:
            return await msg.edit_text(
                "❌ Invalid API Response"
            )

        if not data.get("success"):
            return await msg.edit_text(
                "❌ Failed to fetch Facebook video."
            )

        title = data.get("title", "Facebook Video")

        video_url = (
            data.get("videos", {})
            .get("hd", {})
            .get("url")
        )

        if not video_url:
            video_url = (
                data.get("videos", {})
                .get("sd", {})
                .get("url")
            )

        if not video_url:
            return await msg.edit_text(
                "❌ No video URL found."
            )

        await message.reply_video(
            video=video_url,
            caption=f"🎬 {title}\n\n𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳"
        )

        await msg.delete()

    except requests.exceptions.Timeout:
        await msg.edit_text("❌ API Timeout")

    except Exception as e:
        await msg.edit_text(f"❌ Error:\n{e}")