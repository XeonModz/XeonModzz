from dotenv import load_dotenv
import os
import time


load_dotenv("config.env")

# Retrieve environment variables with safe defaults
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
SUDO = list(map(int, os.environ.get("SUDO", "0").split(',')))
PORT = int(os.environ.get("PORT", 5000))
OG_BOT_NAME = ('𝑅𝒐𝒛𝒆𝒔𓆩♡𓆪')
MODE = os.environ.get("MODE", "Public")
BOT_NAME = os.environ.get("BOT_NAME",OG_BOT_NAME)
ROZE_API= "https://miss-roze-basic-api.onrender.com" # Don't Edit 
RENDER_API_TOKEN = os.environ.get("RENDER_API_TOKEN") # Don't Edit
BOT_LOGO = os.environ.get("BOT_LOGO")
BOT_START_TIME = time.time()
CATBOX_API_URL = "https://catbox.moe/user/api.php" # Don't Edit 
OPENAI = "https://api.openai.com/v1/chat/completions"
GPT_KEY = os.environ.get("OPENAI_API", "0")
MODEL = os.environ.get("MODEL", "gpt-3o-mini")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "0")
COOKIES = os.environ.get("YOUTUBE_COOKIES", "")
OWNER_NAME = os.environ.get("OWNER_NAME", "DOT-007")
OWNER_URL = os.environ.get("OWNER_URL", "https://alosious-benny.vercel.app")
OWNER_ID = int(os.environ.get("OWNER_ID", "7142034518"))
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://roxezzx:AKgJYyXQmzwBtV7l@cluster0.76g2o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL") # Don't Edit
if not API_ID or not API_HASH or not BOT_TOKEN or not SUDO:
    raise ValueError("Missing required environment variables! Check your .env file.")