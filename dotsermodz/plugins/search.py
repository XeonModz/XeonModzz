# Version: 1.0 Beta
# ©️ 2025 DOTSERMODZ ALL RIGHTS RESERVED
from pyrogram import Client, filters
import requests
from dotsermodz import app 
from config import ROZE_API
from dotsermodz.lib.mode import isPrivate
import urllib.parse


@app.on_message(filters.command("img"))
@isPrivate
async def send_image(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a search query. Example: /img cat")
        return
    
    query = " ".join(message.command[1:])
    encoded_query = urllib.parse.quote(query)  
    response = requests.get(ROZE_API + "/bingimg?query="+ encoded_query)
    
    if response.status_code != 200:
        await message.reply_text("Failed to fetch images. Please try again later.")
        return
    
    data = response.json()
    images = data.get("images", [])
    
    if not images:
        await message.reply_text("No images found for the given query.")
        return
    
    for image_url in images:
        await message.reply_photo(photo=image_url, caption=f"Image for: {query}")


@app.on_message(filters.command("wiki"))
@isPrivate
async def wiki_search(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a search query. Usage: /wiki <query>")
        return
    
    query = " ".join(message.command[1:])
    url = ROZE_API + "/wiki?query="+ query
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            summary = data.get("summary", "No information available.")
            reply_text = f"**Query:** {data.get('query', query)}\n\n**Summary:** {summary}"
        else:
            reply_text = "Failed to fetch data. Please try again later."
    except Exception as e:
        reply_text = f"Error: {str(e)}"
    
    await message.reply_text(reply_text)