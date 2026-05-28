# Version: 1.0 Beta
# ©️ 2025 xeonmodz ALL RIGHTS RESERVED
from pyrogram import Client, filters
from pyrogram.types import Message
from xeonmodz import app
from config import BOT_NAME
from xeonmodz.lib.fancy import FANCY_FONTS
from xeonmodz.lib.mode import isPrivate


def apply_fancy(font_map, text):
    return "".join(font_map.get(char, char) for char in text)

def generate_usage_examples(text):
    examples = f"{BOT_NAME}\n\nUsage: /fancy style_number text\n\nExamples:\n"
    for style_num, font_map in FANCY_FONTS.items():
        examples += f"{style_num}: {apply_fancy(font_map, text)}\n"
    return examples

@app.on_message(filters.command("fancy"))
@isPrivate
async def fancy_text(client: Client, message: Message):
    args = message.text.split(maxsplit=2)
    if len(args) < 2:
        await message.reply_text(generate_usage_examples("Hey You!"))
        return

    try:
        style_number = int(args[1])
        text = args[2] if len(args) > 2 else message.reply_to_message.text if message.reply_to_message else None
        if text is None:
            await message.reply_text("Please provide text to style.")
            return
        
        styled_text = apply_fancy(FANCY_FONTS.get(style_number, {}), text)
        await message.reply_text(styled_text or "Style not found.")
    except ValueError:
        await message.reply_text("Invalid style number.")
