import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from dotsermodz import app
from config import GEMINI_API_KEY , SUDO
from dotsermodz.lib.mode import isPrivate

async def send_long_message(message: Message, text: str, chunk_size: int = 3000):
    for i in range(0, len(text), chunk_size):
        await message.reply_text(text[i:i+chunk_size])


@app.on_message(filters.command("gemini"))
@isPrivate
async def gemini_command(client: Client, message: Message):

    if len(message.command) < 2:
        await message.reply_text("Please provide a query after /gemini. Example: `/gemini What is the capital of France?`")
        return

    query = " ".join(message.command[1:])
    thinking_msg = await message.reply_text("Thinking...")  # Save the message object

    try:
        response_text = await get_gemini_response(query)
        if len(response_text) <= 4096:
            await thinking_msg.edit_text(response_text)
        else:
            await thinking_msg.delete()
            await send_long_message(message, response_text)
    except Exception as e:
        await thinking_msg.edit_text(f"An error occurred: {e}")

async def get_gemini_response(query: str) -> str:

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": query
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for bad status codes

    data = response.json()
    
    if data and "candidates" in data and data["candidates"]:
        first_candidate = data["candidates"][0]
        if "content" in first_candidate and "parts" in first_candidate["content"]:
            for part in first_candidate["content"]["parts"]:
                if "text" in part:
                    return part["text"]
    return "No response text found from Gemini."