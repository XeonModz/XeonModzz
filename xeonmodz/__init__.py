# Version: 1.0 Beta
# ©️ 2021 xeonmodz ALL RIGHTS RESERVED
from pyrogram import Client
from pymongo import MongoClient
from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    MONGO_URL,
)



# Connect to MongoDB for accessing plugin database
client = MongoClient(MONGO_URL)
db = client['plugin']
plugindb = db['plugindb']


# Install plugins from database if any exists
def plugins():
    pl = plugindb.find()
    for m in pl:
        try:
            exec(m["url"], globals())
            print(f"Successfully installed: {m['name']}")
        except:
            print("an error")

app = Client(
    "xeonmodz-basebot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root="xeonmodz"), 
)

