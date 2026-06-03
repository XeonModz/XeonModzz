from pyrogram import filters
from xeonmodz import app
import asyncio

ANTI_BOT = set()
WARNINGS = {}


@app.on_message(filters.command("antibot") & filters.group)
async def antibot_toggle(client, message):

    try:
        member = await client.get_chat_member(
            message.chat.id,
            message.from_user.id
        )

        status = str(member.status).lower()

        if (
            "administrator" not in status
            and "creator" not in status
            and "owner" not in status
        ):
            return

    except:
        return

    if len(message.command) != 2:
        return await message.reply_text(
            "Usage:\n"
            "/antibot on\n"
            "/antibot off\n"
            "/antibot status"
        )

    mode = message.command[1].lower()

    if mode == "on":

        ANTI_BOT.add(message.chat.id)

        try:
            await message.react("✅")
        except:
            pass

        await message.reply_text(
            "🤖 AntiBot Enabled"
        )

    elif mode == "off":

        ANTI_BOT.discard(message.chat.id)

        try:
            await message.react("❌")
        except:
            pass

        await message.reply_text(
            "🤖 AntiBot Disabled"
        )

    elif mode == "status":

        try:
            await message.react("ℹ️")
        except:
            pass

        if message.chat.id in ANTI_BOT:

            await message.reply_text(
                "🤖 AntiBot Status: ENABLED"
            )

        else:

            await message.reply_text(
                "🤖 AntiBot Status: DISABLED"
            )


@app.on_message(filters.group & filters.new_chat_members, group=100)
async def antibot_checker(client, message):

    if message.chat.id not in ANTI_BOT:
        return

    me = await client.get_me()

    adder = message.from_user

    if not adder:
        return

    # Ignore admins
    try:

        admin = await client.get_chat_member(
            message.chat.id,
            adder.id
        )

        status = str(admin.status).lower()

        if (
            "administrator" in status
            or "creator" in status
            or "owner" in status
        ):
            return

    except:
        pass

    for member in message.new_chat_members:

        if not member.is_bot:
            continue

        if member.id == me.id:
            continue

        try:

            # Remove added bot
            await client.ban_chat_member(
                message.chat.id,
                member.id
            )

            await client.unban_chat_member(
                message.chat.id,
                member.id
            )

            key = (
                message.chat.id,
                adder.id
            )

            WARNINGS[key] = WARNINGS.get(
                key,
                0
            ) + 1

            warns = WARNINGS[key]

            try:
                await message.react("⚠️")
            except:
                pass

            warn_msg = await message.reply_text(
                f"⚠️ Warning\n\n"
                f"{adder.mention} added a bot.\n"
                f"Warnings: {warns}/3\n\n"
                f"Removed Bot: {member.first_name}"
            )

            await asyncio.sleep(5)

            try:
                await warn_msg.delete()
            except:
                pass

            # Kick user after 3 warnings
            if warns >= 3:

                kick_msg = await message.reply_text(
                    f"🚫 {adder.mention}\n\n"
                    f"Maximum warnings reached.\n"
                    f"Removing user..."
                )

                await client.ban_chat_member(
                    message.chat.id,
                    adder.id
                )

                await client.unban_chat_member(
                    message.chat.id,
                    adder.id
                )

                WARNINGS.pop(
                    key,
                    None
                )

                try:
                    await message.react("🚫")
                except:
                    pass

                await asyncio.sleep(5)

                try:
                    await kick_msg.delete()
                except:
                    pass

        except Exception as e:
            print(
                f"AntiBot Error: {e}"
            )