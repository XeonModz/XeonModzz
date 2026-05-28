# ©️ 2025 xeonmodz ALL RIGHTS RESERVED

import logging
from pyrogram import filters, __version__
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    InputMediaPhoto
)

from xeonmodz.lib.base import IMAGE_LINK
from xeonmodz.lib.mode import isPrivate
from xeonmodz import app
from config import BOT_NAME, OWNER_NAME, OWNER_URL, OWNER_ID


# START COMMAND
@app.on_message(filters.command("start"))
@isPrivate
async def start(client, message):

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
            [
                InlineKeyboardButton("ℹ️ About", callback_data="about"),
                InlineKeyboardButton("👤 Owner Info", callback_data="owner_info")
            ],
            [
                InlineKeyboardButton("📜 Menu", callback_data="menu")
            ]
        ]
    )

    await message.reply_photo(
        photo=IMAGE_LINK,
        caption=caption,
        reply_markup=keyboard
    )

    logging.info(f"Start message sent to {message.chat.id}")


# MENU COMMAND
@app.on_message(filters.command(["menu", "help", "list"]))
@isPrivate
async def menu(client, message):

    ascii_border = f"\n**❍⊷══〘{BOT_NAME}〙═══⊷❍**\n"

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
        "/qr": "Generate QR code",
        "/fancy": "Fancy text generator",
        "/img": "Search images",
        "/wiki": "Wikipedia search",
        "/gdrive": "Google Drive downloader",
        "/pp": "Update profile picture",
        "/gpp": "Update group picture",
        "/install": "Install plugins",
        "/uninstall": "Uninstall plugins",
        "/allplug": "Show all plugins"
    }

    menu_text = f"{ascii_border}\n"
    menu_text += "**🕊️ Available Commands:**\n\n"

    for cmd, desc in commands.items():
        menu_text += f"➤ {cmd} - {desc}\n"

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_start")]
        ]
    )

    await message.reply_photo(
        photo=IMAGE_LINK,
        caption=menu_text,
        reply_markup=keyboard
    )

    logging.info(f"Menu sent to {message.chat.id}")


# OWNER INFO
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


# CALLBACK HANDLER
@app.on_callback_query()
async def cb_handler(client, query: CallbackQuery):

    data = query.data

    # ABOUT
    if data == "about":

        await query.message.edit_text(
            text=(
                f"<b>🤖 {BOT_NAME}</b>\n\n"
                f"<b>○ Creator :</b> <a href='tg://user?id={OWNER_ID}'>This Person</a>\n"
                f"<b>○ Language :</b> <code>Python3</code>\n"
                f"<b>○ Library :</b> "
                f"<a href='https://docs.pyrogram.org/'>Pyrogram {__version__}</a>\n"
                f"<b>○ Source Code :</b> <a href=''>Click here</a>"
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_start")]]
            )
        )

    # MENU
    elif data == "menu":

        ascii_border = f"\n**❍⊷══〘{BOT_NAME}〙═══⊷❍**\n"

        commands = {
            "/start": "Start the bot",
            "/alive": "Check bot status",
            "/menu": "Show available commands",
            "/help": "Show help message",
            "/list": "Show command list",
            "/ping": "Check bot latency"
        }

        menu_text = f"{ascii_border}\n"
        menu_text += "**🕊️ Available Commands:**\n\n"

        for cmd, desc in commands.items():
            menu_text += f"➤ {cmd} - {desc}\n"

        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("⬅️ Back", callback_data="back_to_start")]
            ]
        )

        await query.message.edit_media(
            media=InputMediaPhoto(
                media=IMAGE_LINK,
                caption=menu_text
            ),
            reply_markup=keyboard
        )

    # OWNER INFO
    elif data == "owner_info":
        await owner_info(client, query)

    # BACK BUTTON
    elif data == "back_to_start":

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
                [
                    InlineKeyboardButton("ℹ️ About", callback_data="about"),
                    InlineKeyboardButton("👤 Owner Info", callback_data="owner_info")
                ],
                [
                    InlineKeyboardButton("📜 Menu", callback_data="menu")
                ]
            ]
        )

        await query.message.edit_media(
            media=InputMediaPhoto(
                media=IMAGE_LINK,
                caption=caption
            ),
            reply_markup=keyboard
        )