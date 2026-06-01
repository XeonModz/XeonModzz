from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserAdminInvalid, PeerIdInvalid, ChatAdminRequired, UserNotParticipant
from xeonmodz import app

@app.on_message(filters.command("kick") & filters.group)
async def kick_user(client: Client, message: Message):

    member = await client.get_chat_member(
        message.chat.id,
        message.from_user.id
    )

    if member.status not in (
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER
    ):
        return await message.reply(
            "You need to be an admin to use this command."
        )

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id

    elif len(message.command) > 1:
        username = message.command[1].lstrip("@")

        try:
            user = await client.get_users(username)
            user_id = user.id

        except Exception:
            return await message.reply(
                "Couldn't find that user."
            )

    else:
        return await message.reply(
            "Reply to a user's message or mention their username to kick them."
        )

    try:
        target = await client.get_chat_member(
            message.chat.id,
            user_id
        )

        if target.status == ChatMemberStatus.OWNER:
            return await message.reply(
                "I can't kick the group owner."
            )

        if target.status == ChatMemberStatus.ADMINISTRATOR:
            return await message.reply(
                "I can't kick an admin."
            )

        await client.ban_chat_member(
            message.chat.id,
            user_id
        )

        await client.unban_chat_member(
            message.chat.id,
            user_id
        )

        await message.reply(
            "✅ User has been kicked."
        )

    except UserAdminInvalid:
        await message.reply(
            "I can't kick this user."
        )

    except ChatAdminRequired:
        await message.reply(
            "I need admin rights with ban permissions."
        )

    except UserNotParticipant:
        await message.reply(
            "That user is not in this group."
        )

    except PeerIdInvalid:
        await message.reply(
            "Invalid user."
        )

    except Exception as e:
        await message.reply(
            f"Error: {e}"
        )