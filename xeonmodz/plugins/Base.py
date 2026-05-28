# Version: 1.0 Beta
# ©️ 2025 xeonmodz ALL RIGHTS RESERVED
import logging
from pyrogram import Client, filters
from xeonmodz.lib.base import IMAGE_LINK
from xeonmodz.lib.mode import isPrivate
from xeonmodz import app
from config import BOT_NAME, OWNER_NAME, OWNER_URL, OWNER_ID 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import __version__




# Define a command to send a start message
@app.on_message(filters.command("start"))
@isPrivate
async def start(client, message):
    caption = (
        f"**I am {BOT_NAME}**\n"
        f"✨ Created by: [{OWNER_NAME}]({OWNER_URL})\n\n"
        "🔹 I can be used as a base to build powerful bots.\n"
        "🔹 Fast, lightweight, and easy to customize.\n"
        "🔥 Stay tuned for updates!\n\n"
        f"🚀 Powered by {OWNER_NAME}"
    )
    
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("ℹ️ About", callback_data="about"), InlineKeyboardButton("👤 Owner Info", callback_data="owner_info")],
            [InlineKeyboardButton("📜 Menu", callback_data="menu")]
        ]
    )
    await message.react("🕊️")
    await message.reply_photo(IMAGE_LINK, caption=caption, reply_markup=keyboard)
    logging.info(f"Start message sent to {message.chat.id}")

# Define the menu command
@app.on_message(filters.command(["menu", "help"]))
@isPrivate
async def menu(client, message):
    ascii_border = f"\n**❍⊷══〘{BOT_NAME}〙═══⊷❍**\n"   
    commands = {
        "𝐵𝒂𝒔𝒊𝒄 𝐶𝒎𝒅\n"
        "/start": "Start the bot",
        "/alive": "Check bot status",
        "/menu": "Show available commands",
        "/eval": "Evaluate Python code",
        "/help": "Show help message",
        "/id": "Get chat ID",
        "/ping": "Check bot latency",
        "/reboot": "Restart the bot",
        "/sysinfo": "Show system info",
        "/stats": "Show bot statistics",
        "/uptime": "Show bot uptime",
        "/shutdown": "Shutdown the bot",
        "/shell": "Run shell commands\n",
        "𝑈𝒕𝒊𝒍𝒊𝒕𝒚\n"
        "/insta": "Instagram post download",
        "/teradl": "Terabox video download",
        "/pinterest": "Pinterest image download",
        "/upload": "Image to URL",
        "/qr": "Generate QR code",
        "/fancy": "Fancy text generator",
        "/img": "Search images",
        "/wiki": "Search Wikipedia\n",
        "/gdrive": "Google Drive file download",
        "𝑀𝒂𝒏𝒂𝒈𝒆 𝒑𝒓𝒐𝒇𝒊𝒍𝒆 𝒑𝒊𝒄𝒕𝒖𝒓𝒆\n"
        "/pp": "Update profile picture",
        "/gpp": "Update group profile picture\n",
        "𝑀𝒂𝒏𝒂𝒈𝒆 𝒆𝒙-𝒑𝒍𝒖𝒈𝒊𝒏𝒔 𝒇𝒓𝒐𝒎 𝒈𝒊𝒔𝒕𝒔 𝒖𝒓𝒍\n"
        "/install": "Install plugins",
        "/uninstall": "Uninstall plugins",
        "/allplug": "Show all plugins"
        
    }

    menu_text = f"{ascii_border}\n\n"
    menu_text += "**🕊️ Available Commands:**\n"
    menu_text += "━━━━━━━━━━━━━━━━━━━━━━\n"
    
    for cmd, desc in commands.items():
        menu_text += f"**{cmd}** - {desc}\n"

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_start")]]
    )
    
    await message.reply_photo(IMAGE_LINK, caption=menu_text)
    logging.info(f"Menu sent to {message.chat.id}")

# Define owner info command
async def owner_info(client, query):
    await query.message.edit_text(
        text=(
            f"<b>{BOT_NAME}</b>\n"
            f"<b>👤 Owner Information</b>\n\n"
            f"○ Name : [{OWNER_NAME}]({OWNER_URL})\n"
            f"○ User ID : <code>{OWNER_ID}</code>\n"
            f"○ Contact : <a href='tg://user?id={OWNER_ID}'>Click here</a>"
        ),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_start")]]
        )
    )


# Callback handler
@app.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text=(
                f"<b>🤖{BOT_NAME}</b>\n\n"
                f"<b>○ Creator : <a href='tg://user?id={OWNER_ID}'>This Person</a>\n"
                f"○ Language : <code>Python3</code>\n"
                f"○ Library : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio {__version__}</a>\n"
                f"○ Source Code : <a href='https://github.com/Dot-ser/PyroRose-V1/'>Click here</a>\n"
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_start")]]
            )
        )
    elif data == "menu":
        await menu(client, query.message)
    elif data == "start":
        await start(client, query.message)
    elif data == "owner_info":
        await owner_info(client, query)
    elif data == "back_to_start":  # Ensures it goes back to the original message
        caption = (
            f"**🤖 I am {BOT_NAME}**\n"
            f"✨ Created by: [{OWNER_NAME}]({OWNER_URL})\n\n"
            "🔹 I can be used as a base to build powerful bots.\n"
            "🔹 Fast, lightweight, and easy to customize.\n"
            "🔥 Stay tuned for updates!\n\n"
            f"🚀 Powered by {OWNER_NAME}"
        )
        
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("ℹ️ About", callback_data="about"), InlineKeyboardButton("👤 Owner Info", callback_data="owner_info")],
                [InlineKeyboardButton("📜 Menu", callback_data="menu")]
            ]
        )
        await query.message.edit_caption(caption, reply_markup=keyboard)