import requests 
import json
from pyrogram import Client, filters
from pyrogram.types import Message
from config import OPENAI, MODEL, GPT_KEY
def get_gpt_response(user_input: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": user_input}],
        "temperature": 0.7,
    }
    
    headers = {
        "Authorization": f"Bearer {GPT_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(OPENAI, headers=headers, json=payload)
    response_data = response.json()
    return response_data["choices"][0]["message"]["content"]