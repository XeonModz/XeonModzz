from xeonmodz import app
from config import SUDO 
from xeonmodz.lib.base import sudo_usernames
from pyrogram import Client, filters

# Command to get the list of sudo users
@app.on_message(filters.command("getsudo") & filters.user(SUDO))  
async def getsudo(client, message):
    sudo_users = await sudo_usernames(app) 
    caption = (
        f"ALL SUDO USERS\n\n"
        f"{sudo_users}" 
    )
    await message.reply(caption)


@app.on_message(filters.command("hello") & filters.user(SUDO))
async def hello(client, message):
    
    await message.reply("Hello, Sudo User!")