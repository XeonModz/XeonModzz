from pyrogram import filters
from pyrogram.types import ChatPermissions
from xeonmodz import app


@app.on_message(filters.command("mute") & filters.group)
async def mute_group(client, message):

    try:

        await client.set_chat_permissions(
            message.chat.id,
            ChatPermissions()
        )

        try:
            await message.react("🔇")
        except:
            pass

    except Exception as e:

        await message.reply_text(
            f"Error:\n{e}"
        )


@app.on_message(filters.command("unmute") & filters.group)
async def unmute_group(client, message):

    try:

        await client.set_chat_permissions(
            message.chat.id,
            ChatPermissions(
                can_send_messages=True
            )
        )

        try:
            await message.react("🔊")
        except:
            pass

    except Exception as e:

        await message.reply_text(
            f"Error:\n{e}"
        )