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
OG_BOT_NAME = ('𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳')
MODE = os.environ.get("MODE", "Public")
BOT_NAME = os.environ.get("BOT_NAME", OG_BOT_NAME)
XEON_INSTA_API = "https://xeon-insta-api.onrender.com"
XEON_PIN_API = "https://xeon-pin-api.onrender.com"
RENDER_API_TOKEN = os.environ.get("RENDER_API_TOKEN")
BOT_LOGO = os.environ.get("BOT_LOGO")
BOT_START_TIME = time.time()
COOKIES = os.environ.get("YOUTUBE_COOKIES", "")
OWNER_NAME = os.environ.get("OWNER_NAME", "XeonModz")
OWNER_URL = os.environ.get("OWNER_URL","https://xeonmodz-online.onrender.com")
IMAGE_LINK = os.environ.get("IMAGE_LINK","https://i.ibb.co/wHnkzmd/temp.jpg")
VIDEO_URL = os.environ.get("VIDEO_URL","https://your-default-video-url.mp4")
OWNER_ID = int(os.environ.get("OWNER_ID", "7833143784"))

MONGO_URL = os.environ.get("MONGO_URL","mongodb+srv://Xeon:XeonGamingYT@xeon.dig9eor.mongodb.net/myDatabase?retryWrites=true&w=majority&appName=Xeon")

RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")

if not API_ID or not API_HASH or not BOT_TOKEN:
    raise ValueError("Missing required environment variables! Check your .env file.")