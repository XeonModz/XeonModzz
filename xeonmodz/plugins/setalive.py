from pyrogram import filters
from xeonmodz import app
from xeonmodz.lib.mode import isPrivate
from xeonmodz.lib.mongo import save_alive

@app.on_message(filters.command("setalive"))
@isPrivate
async def setalive(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/setalive your alive message"
        )

    text = message.text.split(None, 1)[1]

    save_alive(text)

    await message.reply_text(
        "✅ Alive message saved."
    )