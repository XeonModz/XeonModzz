# Version: 1.0 Beta
# ©️ 2025 DOTSERMODZ ALL RIGHTS RESERVED
from dotsermodz.keep import web 
from dotsermodz import app, plugindb 
from config import RENDER_EXTERNAL_URL
from dotsermodz.lib.base import strt_msgs , uzumaki
from pyrogram import idle
import logging
import asyncio
import requests 


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Function to start the bot and keep it alive
async def main():
     await app.start() 
     await uzumaki()
     web.yuji_itadori()
     if RENDER_EXTERNAL_URL:                                    # Edit there if you are not using render.com or not required    
        asyncio.create_task(web.luffy(RENDER_EXTERNAL_URL))     # Keep pinging the host Only if bot is hosted on render.com                
     await idle()      

if __name__ == "__main__":
    print(strt_msgs)  
# Import all plugins from the plugins database    
    pl = plugindb.find()
    for m in pl:
        try:
            response = requests.get(m["url"].replace("github.com", "githubusercontent.com") + "/raw")
            exec(response.text, globals())
            print(f"Successfully installed: {m['name']}")
        except:
            print("An error occurred while installing:", m["name"])


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())          
