# Version: 1.0 Beta
# ©️ 2025 xeonmodz ALL RIGHTS RESERVED
from pyrogram import Client, filters
from pyrogram.types import Message
from config import SUDO, MODE


def is_admin(user_id: int) -> bool:
    return user_id in SUDO

def isPrivate(func):
    async def wrapper(client: Client, message: Message):
        if MODE.lower() == 'public' or is_admin(message.from_user.id):
            await func(client, message)
        else:
            await message.reply("This bot is private and restricted to SUDO only.")
    return wrapper




