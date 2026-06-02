from pyrogram import filters
from xeonmodz import app
from xeonmodz.lib.mongo import usersdb

@app.on_message(filters.private, group=100)
async def save_user(client, message):

    if not message.from_user:
        return

    try:

        usersdb.update_one(
            {"user_id": message.from_user.id},
            {
                "$set": {
                    "user_id": message.from_user.id,
                    "name": message.from_user.first_name,
                    "username": message.from_user.username
                }
            },
            upsert=True
        )

    except Exception as e:
        print(f"User Save Error: {e}")