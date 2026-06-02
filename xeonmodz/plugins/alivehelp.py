from pyrogram import filters
from xeonmodz import app
from xeonmodz.lib.mode import isPrivate

@app.on_message(filters.command("alivehelp"))
@isPrivate
async def alivehelp(client, message):

    await message.reply_text(
        """
Available Variables

$user
$botname
$uptime
$users
$ram
$totalram

Media:

$media:https://url.mp4

Example:

/setalive Hello $user
"""
    )