# Version: 1.0 Beta
# ©️ 2025 xeonmodz ALL RIGHTS RESERVED
from xeonmodz import app 
from config import BOT_NAME
from xeonmodz.lib.mode import isPrivate
from xeonmodz.lib import base
from pyrogram import filters
import time
import psutil
from datetime import timedelta

# Stats command to get system stats
@app.on_message(filters.command("stats"))
@isPrivate
async def stats(client, message):
    # Get CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)
    # Get RAM usage
    ram_usage = psutil.virtual_memory().percent
    # Get system uptime
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_str = str(timedelta(seconds=int(uptime_seconds)))

    # Create the response message
    response = f"**{BOT_NAME} **\n\n"
    response += f"**System Stats:**\n"
    response += f"**🖥️ CPU Usage:** {cpu_usage}%\n"
    response += f"**📈 RAM Usage:** {ram_usage}%\n"
    response += f"**⏳ Uptime:** {uptime_str}\n"

    await message.reply_text(response)

# uptime command to get the bot uptime
@app.on_message(filters.command("uptime"))
@isPrivate
async def stats(client, message):
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_str = str(timedelta(seconds=int(uptime_seconds)))
    os_uptime = base.get_os_uptime()


    # Create the response message
    response = f"**{BOT_NAME} **\n"
    response += f"**⏳ Uptime:** {uptime_str}\n"
    response += f"**OS BOOT TIME** {os_uptime}\n"

    await message.reply_text(response)

