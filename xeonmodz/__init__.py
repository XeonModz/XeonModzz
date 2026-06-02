# Version: 1.0 Beta
# ©️ 2025 XeonModz ALL RIGHTS RESERVED

from pyrogram import Client
from pymongo import MongoClient

from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    MONGO_URL,
)

# MongoDB
client = MongoClient(MONGO_URL)

db = client["plugin"]

plugindb = db["plugindb"]


def plugins():

    pl = plugindb.find()

    for m in pl:

        try:

            exec(
                m["url"],
                globals()
            )

            print(
                f"Successfully installed: "
                f"{m['name']}"
            )

        except Exception as e:

            print(
                f"Plugin Error "
                f"{m['name']}: {e}"
            )


app = Client(
    "xeonmodz-basebot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(
        root="xeonmodz.plugins"
    ),
)