# ©️ 2025 xeonmodz ALL RIGHTS RESERVED

import logging
from pyrogram import filters, __version__
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from xeonmodz.lib.mode import isPrivate
from xeonmodz import app
from config import BOT_NAME, OWNER_NAME, OWNER_URL, OWNER_ID, IMAGE_LINK


def start_caption():
    return (
        f"🤖 I am {BOT_NAME}\n"
        f"✨ Created by: {OWNER_NAME}\n\n"
        "🔹 I can be used as a base to build powerful bots.\n"
        "🔹 Fast, lightweight, and easy to customize.\n"
        "🔹 Stay tuned for updates!\n\n"
        f"🚀 Powered by {OWNER_NAME}"
    )


def start_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("ℹ️ About", callback_data="about"),
                InlineKeyboardButton("👤 Owner Info", callback_data="owner_info")
            ],
            [
                InlineKeyboardButton("📜 Menu", callback_data="menu")
            ]
        ]
    )


@app.on_message(filters.command("start"))
@isPrivate
async def start(client, message):

    print(f"IMAGE_LINK = {IMAGE_LINK}")

    try:
        await message.reply_photo(
            photo=IMAGE_LINK,
            caption=start_caption(),
            reply_markup=start_buttons()
        )
    except Exception as e:
        print(f"PHOTO ERROR: {e}")

        await message.reply_text(
            start_caption(),
            reply_markup=start_buttons()
        )


@app.on_message(filters.command(["menu", "help", "list"]))
@isPrivate
async def menu(client, message):

    commands = {
        "/start": "Start the bot",
        "/alive": "Check bot status",
        "/menu": "Show available commands",
        "/help": "Show help message",
        "/list": "Show command list",
        "/eval": "Evaluate Python code",
        "/id": "Get chat ID",
        "/ping": "Check bot latency",
        "/reboot": "Restart the bot",
        "/sysinfo": "Show system info",
        "/stats": "Show bot statistics",
        "/uptime": "Show bot uptime",
        "/shutdown": "Shutdown the bot",
        "/shell": "Run shell commands",
        "/insta": "Instagram downloader",
        "/teradl": "Terabox downloader",
        "/pinterest": "Pinterest downloader",
        "/upload": "Image uploader",
        "/fancy": "Fancy text generator",
        "/img": "Search images",
        "/pp": "Update profile picture",
        "/gpp": "Update group picture",
        "/install": "Install plugins",
        "/uninstall": "Uninstall plugins",
        "/allplug": "Show all plugins"
    }

    text = f"❍⊷══〘{BOT_NAME}〙══⊷❍\n\n🕊️ Available Commands:\n\n"

    for cmd, desc in commands.items():
        text += f"➤ {cmd} - {desc}\n"

    await message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_start")]]
        )
    )


@app.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    await query.answer()

    if query.data == "about":
        await query.message.edit_text(
            f"🤖 {BOT_NAME}\n\n"
            f"Creator: {OWNER_NAME}\n"
            f"Library: Pyrogram {__version__}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_start")]]
            )
        )

    elif query.data == "owner_info":
        await query.message.edit_text(
            f"👤 Owner: {OWNER_NAME}\n"
            f"ID: {OWNER_ID}\n"
            f"URL: {OWNER_URL}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_start")]]
            )
        )

    elif query.data == "menu":
        await query.message.edit_text(
            "🕊️ Available Commands:\n\n"
            "➤ /start\n"
            "➤ /menu\n"
            "➤ /help\n"
            "➤ /list\n"
            "➤ /ping",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_start")]]
            )
        )

    elif query.data == "back_to_start":
        await query.message.edit_text(
            start_caption(),
            reply_markup=start_buttons()
        )

logging.info("Menu plugin loaded successfully")
print("BASE PLUGIN LOADED")