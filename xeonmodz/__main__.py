from xeonmodz.keep import web
from xeonmodz.lib.mongo import usersdb
from pyrogram import filters, idle
from xeonmodz import app, plugindb
from config import RENDER_EXTERNAL_URL
from xeonmodz.lib.base import strt_msgs, uzumaki
import logging
import asyncio
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


@app.on_message(filters.private)
async def save_user(client, message):

    if not message.from_user:
        return

    usersdb.update_one(
        {"user_id": message.from_user.id},
        {
            "$set": {
                "name": message.from_user.first_name
            }
        },
        upsert=True
    )


async def main():

    await app.start()

    await uzumaki()

    web.yuji_itadori()

    if RENDER_EXTERNAL_URL:
        asyncio.create_task(
            web.luffy(RENDER_EXTERNAL_URL)
        )

    await idle()


if __name__ == "__main__":

    print(strt_msgs)

    pl = plugindb.find()

    for m in pl:

        try:

            response = requests.get(
                m["url"]
                .replace(
                    "github.com",
                    "githubusercontent.com"
                )
                + "/raw"
            )

            exec(response.text, globals())

            print(
                f"Successfully installed: {m['name']}"
            )

        except Exception as e:

            print(
                f"An error occurred while installing "
                f"{m['name']}: {e}"
            )

    loop = asyncio.get_event_loop()

    loop.run_until_complete(main())