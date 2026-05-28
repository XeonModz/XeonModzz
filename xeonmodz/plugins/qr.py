# Version: 1.0 Beta
# ©️ 2025 xeonmodz ALL RIGHTS RESERVED
from xeonmodz.lib.mode import isPrivate
from xeonmodz.lib.download import fetch_qr, qr_del  
from xeonmodz import app
from config import BOT_NAME 
from pyrogram import  filters


@app.on_message(filters.command("qr"))
@isPrivate
async def generate_qr(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide text to generate QR code.\nUsage: `/qr your text`", quote=True)
        return
    
    text = " ".join(message.command[1:])
    file_path = fetch_qr(text)
    
    if file_path:
        await message.reply_photo(file_path, caption=f"{BOT_NAME}\nQR Code for: `{text}`")
        qr_del(file_path)
    else:
        await message.reply_text("Failed to generate QR code. Please try again later.", quote=True).
