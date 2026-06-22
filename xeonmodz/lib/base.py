# Version: 1.0 Beta
# ©️ 2026 XeonModz ALL RIGHTS RESERVED

from xeonmodz import app
from config import SUDO, BOT_NAME, BOT_LOGO, MODE, OWNER_ID
from io import BytesIO
import requests
import time
import psutil

strt_msgs = """ 
\033[36m___________________________________________________________
\033[36m-----------------------------------------------------------
\033[36m-----------------------------------------------------------

\033[34m██╗░░██╗███████╗░█████╗░███╗░░██╗
\033[34m╚██╗██╔╝██╔════╝██╔══██╗████╗░██║
\033[34m░╚███╔╝░█████╗░░██║░░██║██╔██╗██║
\033[34m░██╔██╗░██╔══╝░░██║░░██║██║╚████║
\033[34m██╔╝╚██╗███████╗╚█████╔╝██║░╚███║
\033[34m╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚══╝

\033[36m-----------------------------------------------------------
\033[33m🇽​​​​​🇪​​​​​🇴​​​​​🇳 🇧​​​​​🇴​​​​​🇹 - 🇸​​​​​🇹​​​​​🇦​​​​​🇷​​​​​🇹​​​​​🇮​​​​​🇳​​​​​🇬​​​​​...
\033[35mDeveloper : \033[32m[XeonModz](https://xeonmodz-online.onrender.com)
\033[35mVersion   : \033[37m1.0 Beta
\033[35mPython    : \033[37m3.9.6
\033[35mLibrary   : \033[37mPyrogram & Pyrofork
\033[35mDatabase  : \033[37mMongoDB
\033[31m©️ 2025 XeonModz ALL RIGHTS RESERVED
\033[36m-----------------------------------------------------------
\033[36m-----------------------------------------------------------
\033[36m___________________________________________________________
\033[0m
"""

star = "✬"


async def sudo_usernames(app):
    sudo_users = []

    for user_id in SUDO:
        try:
            user = await app.get_users(user_id)
            name = f"@{user.username}" if user.username else user.first_name
            sudo_users.append(name)
        except Exception:
            sudo_users.append(str(user_id))

    return ", ".join(sudo_users)


def get_os_uptime():
    boot_time = psutil.boot_time()
    current_time = time.time()
    uptime_seconds = current_time - boot_time

    days = uptime_seconds // (24 * 3600)
    hours = (uptime_seconds % (24 * 3600)) // 3600
    minutes = (uptime_seconds % 3600) // 60

    return f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes"


async def uzumaki():
    sudo_str = await sudo_usernames(app)

    message = (
        f"**╭═══{BOT_NAME}═══⊷❍**\n"
        f"**┃{star}│➥Version:** 1.0 Beta\n"
        f"**┃{star}│➥Python:** 3.9.6\n"
        f"**┃{star}│➥Library:** Pyrogram\n"
        f"**┃{star}│➥Database:** MongoDB\n"
        f"**┃{star}│➥Developer:** [XEON](vercel.app)\n"
        f"**╰═════════════════⊷**\n\n"
        f"**╭══════⊷❍**\n"
        f"**┃{star}│MODE:** {MODE}\n"
        f"**┃{star}│OWNER:** <a href='tg://user?id={OWNER_ID}'>XEON</a>\n"
        f"**┃{star}│SUDO:** {sudo_str}\n"
        f"**╰═══⊷**"
    )

    for sudo in SUDO:
        try:
            await app.send_photo(sudo, photo=IMAGE_LINK, caption=message)
        except Exception as e:
            print(f"Failed to send message to {sudo}: {e}")


# real skill issue meet here :)
# Useless function :)
def satorugojo():
    try:
        image_url = "https://i.ibb.co/KpT0ZBHk/photo-2026-06-02-06-07-00-7646675704108548120.jpg"
        response = requests.get(image_url)

        if response.status_code == 200:
            return BytesIO(response.content)

        return None

    except Exception as e:
        print(f"Error fetching image: {e}")
        return None


image_data = None if BOT_LOGO else satorugojo()
IMAGE_LINK = BOT_LOGO if BOT_LOGO else image_data


def sung_jinwoo():
    if BOT_LOGO:
        try:
            response = requests.get(BOT_LOGO, timeout=15)

            if (
                response.status_code == 200
                and "image" in response.headers.get("Content-Type", "")
            ):
                return BytesIO(response.content)

            else:
                print("BOT_LOGO URL is invalid or not an image. Falling back to default.")

        except Exception:
            print("Error fetching BOT_LOGO, Falling back to default.")

    return satorugojo()
