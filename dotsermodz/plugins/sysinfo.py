# Version: 1.0 Beta
# ©️ 2025 DOTSERMODZ ALL RIGHTS RESERVED
import platform
import psutil
from pyrogram import filters
from dotsermodz import app 
from config import BOT_NAME
from dotsermodz.lib.mode import isPrivate

# This command will show the system information of the bot
@app.on_message(filters.command("sysinfo"))
@isPrivate
async def send_system_info(client, message):
   
    uname = platform.uname()
    sys_info = (
        f"**❍⊷══〘{BOT_NAME}〙═══⊷❍**\n\n"
        f"🖥 **System Information**\n"
        f"**System**: {uname.system}\n"
        f"**Node Name**: {uname.node}\n"
        f"**Release**: {uname.release}\n"
        f"**Version**: {uname.version}\n"
        f"**Machine**: {uname.machine}\n"
        f"**Processor**: {uname.processor}\n"
    )

    memory = psutil.virtual_memory()
    mem_info = (
        f"💾 **Memory Information**\n"
        f"**Total**: {memory.total / (1024 ** 3):.2f} GB\n"
        f"**Available**: {memory.available / (1024 ** 3):.2f} GB\n"
        f"**Used**: {memory.used / (1024 ** 3):.2f} GB\n"
        f"**Percentage**: {memory.percent}%\n"
    )

    await message.reply(f"{sys_info}\n{mem_info}")

