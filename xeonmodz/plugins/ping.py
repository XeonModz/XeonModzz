# Version: 1.0 Beta
# ©️ 2025 xeonmodz ALL RIGHTS RESERVED
from xeonmodz import app
from xeonmodz.lib.mode import isPrivate
from pyrogram import filters
import time

@app.on_message(filters.command("ping"))
@isPrivate
async def ping_command(app, message):
    start_time = time.time()
    reply = await message.reply_text("Pinging...")
    end_time = time.time()
    response_time = int((end_time - start_time) * 1000)
    pingmsg = f"Response time: {response_time} ms"
    await reply.edit_text(pingmsg)
    