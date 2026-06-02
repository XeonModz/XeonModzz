import os
from pymongo import MongoClient
from config import MONGO_URL

client = MongoClient(MONGO_URL)
# Parse database name from URI or use default
if '/' in MONGO_URL.rsplit('@', 1)[-1]:
    db_name = MONGO_URL.rsplit('/', 1)[-1].split('?', 1)[0] or "xeonmodz"
else:
    db_name = "xeonmodz"
db = client[db_name]

usersdb = db["users"]

def save_alive(text):
    db.alive.update_one(
        {},
        {"$set": {"text": text}},
        upsert=True
    )

def get_alive():
    data = db.alive.find_one({})
    return data.get("text") if data else None


def save_yt_cookies(data: str):
    db.yt_cookies.update_one({}, {"$set": {"cookies": data}}, upsert=True)

def get_yt_cookies() -> str:
    doc = db.yt_cookies.find_one({})
    return doc["cookies"] if doc and "cookies" in doc else None
