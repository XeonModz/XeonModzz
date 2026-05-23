# Version: 1.0 Beta
# ©️ 2025 DOTSERMODZ ALL RIGHTS RESERVED
from dotsermodz import app 
from config import BOT_NAME
from dotsermodz.lib import base
from dotsermodz.lib.mode import isPrivate
from pyrogram import filters

star = "✬"

@app.on_message(filters.command("alive"))
@isPrivate
async def alive(client, message):
    # Get OS uptime
    os_uptime = base.get_os_uptime()

    # Define the response message
    response_text = (
    f"**╭═══〘{BOT_NAME}〙═══⊷❍**\n"
    f"┃{star}│✅ **Bot Status: I'm Alive!**\n"
    f"┃{star}│🤖 **Bot Name:** {client.me.first_name}\n"
    f"┃{star}│🆔 **Username:** @{client.me.username}\n"
    f"┃{star}│🕒 **OS Uptime:** {os_uptime}\n"
    f"┃{star}│🚀 Powered by DOT-007\n"
    f"╰═════════════════⊷"
    )

    await message.reply_photo(base.IMAGE_LINK, caption=response_text)


"""
# Version: 1.0 Beta
# ©️ 2025 DOTSERMODZ ALL RIGHTS RESERVED
from dotsermodz import app , BOT_NAME, BOT_START_TIME 
from dotsermodz.lib.base import IMAGE_LINK
from dotsermodz.lib.mode import isPrivate
from pyrogram import filters
import time

star = "✬" 

@app.on_message(filters.command("alive"))
@isPrivate
async def alive(client, message):
    # Calculate uptime
    uptime = time.time() - BOT_START_TIME
    uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime))

    # Define the response message
    response_text = (
    f"**╭═══〘{BOT_NAME}〙═══⊷❍**\n"
    f"┃{star}│✅ **Bot Status: I'm Alive!**\n"
    f"┃{star}│🤖 **Bot Name:** {client.me.first_name}\n"
    f"┃{star}│🆔 **Username:** @{client.me.username}\n"
    f"┃{star}│⏳ **Uptime:** {uptime_str}\n"
    f"┃{star}│🚀 Powered by DOT-007\n"
    f"╰═════════════════⊷"
                    )

    await message.reply_photo(IMAGE_LINK,caption=response_text)


"""