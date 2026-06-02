from pyrogram import filters
from xeonmodz import app
from xeonmodz.lib.mode import isPrivate
from xeonmodz.lib.mongo import get_alive, usersdb
from config import BOT_NAME
import psutil
import time


BOT_START_TIME = time.time()


@app.on_message(filters.command("alive"))
@isPrivate
async def alive(client, message):

    template = get_alive()

    if not template:
        return await message.reply_text(
            "❌ No alive message set.\n\nUse /setalive first."
        )

    total_users = usersdb.count_documents({})

    uptime = time.time() - BOT_START_TIME
    uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime))

    ram_used = round(psutil.virtual_memory().used / (1024**3), 2)
    ram_total = round(psutil.virtual_memory().total / (1024**3), 2)

    template = template.replace(
        "$user",
        message.from_user.mention
    )

    template = template.replace(
        "$botname",
        BOT_NAME
    )

    template = template.replace(
        "$mode",
        "Private"
    )

    template = template.replace(
        "$uptime",
        uptime_str
    )

    template = template.replace(
        "$users",
        str(total_users)
    )

    template = template.replace(
        "$ram",
        str(ram_used)
    )

    template = template.replace(
        "$totalram",
        str(ram_total)
    )

    media_url = None

    if "$media:" in template:

        media_url = (
            template.split("$media:")[1]
            .split("\n")[0]
            .strip()
        )

        template = template.replace(
            f"$media:{media_url}",
            ""
        ).strip()

    try:

        if media_url:

            await message.reply_video(
                video=media_url,
                caption=template
            )

        else:

            await message.reply_text(template)

    except Exception as e:

        await message.reply_text(
            f"Alive Error:\n{e}"
        )