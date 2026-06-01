# # Version: 1.0 Beta
# # ©️ 2025 xeonmodz ALL RIGHTS RESERVED

# from functools import wraps
# from pyrogram import Client
# from pyrogram.types import Message
# from config import SUDO, MODE


# def is_admin(user_id: int) -> bool:
#     return user_id in SUDO


# def isPrivate(func):
#     @wraps(func)
#     async def wrapper(client: Client, message: Message):
#         if MODE.lower() == "public":
#             return await func(client, message)

#         if message.from_user and is_admin(message.from_user.id):
#             return await func(client, message)

#         return await message.reply_text(
#             "This bot is private and restricted to SUDO only."
#         )

#     return wrapper




# xeonmodz/lib/mode.py

from functools import wraps
from pyrogram import Client
from pyrogram.types import Message
from config import SUDO

BOT_MODE = "public"


def set_mode(mode):
    global BOT_MODE
    BOT_MODE = mode.lower()


def get_mode():
    return BOT_MODE


def is_admin(user_id: int) -> bool:
    return user_id in SUDO


def isPrivate(func):
    @wraps(func)
    async def wrapper(client: Client, message: Message):
        if BOT_MODE == "public":
            return await func(client, message)

        if message.from_user and is_admin(message.from_user.id):
            return await func(client, message)

        return await message.reply_text(
            "This bot is private and restricted to SUDO only."
        )

    return wrapper