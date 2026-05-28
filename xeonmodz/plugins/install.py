# Version: 1.0 Beta
# ©️ 2025 xeonmodz ALL RIGHTS RESERVED
from xeonmodz import app , plugindb
from config import SUDO
from pyrogram import filters
import requests

@app.on_message(filters.command("install") & filters.user(SUDO))
async def install_plugins(client, message):
    if len(message.command) < 3:
        await message.reply("Example: /install gist_link plugin_name")
        return
      
    cmd = message.command[1]    
    name = message.command[2]
    
    if plugindb.find_one({"name": name}) or plugindb.find_one({"url": cmd}):
        await message.reply("it's already added")
  
    if not cmd.startswith("https://gist.github.com/"):
        await message.reply("Check Your URL:)")
        return
    response = requests.get(cmd.replace("github.com", "githubusercontent.com") + "/raw")
    try:
        exec(response.text, globals())
        plugindb.insert_one({"name": name, "url": cmd})
        await message.reply("Successfully installed")
    except Exception as e:
        await message.reply(f"Error: {e}")
            

@app.on_message(filters.command("remove") & filters.user(SUDO))
async def remove_plugins(client, message):
    if len(message.command) < 2:
        await message.reply("Usage: /remove plugin_name")
        return

    name = message.command[1]
    
    plugin_entry = plugindb.find_one({"name": name})
    if not plugin_entry:
        await message.reply("Plugin not found!")
        return

    try:
        # Remove from database
        plugindb.delete_one({"name": name})
        
        # Unload the plugin
        if name in globals():
            del globals()[name]
        
        await message.reply(f"Successfully removed **{name}**")
    except Exception as e:
        await message.reply(f"Error removing plugin: {e}")


@app.on_message(filters.command("allplug") & filters.user(SUDO))
async def view_plugins(client, message):
    plugins = plugindb.find({}, {"name": 1, "_id": 0})  # Get all plugin names
    plugin_list = [plugin["name"] for plugin in plugins]

    if not plugin_list:
        await message.reply("No plugins installed!")
        return
    
    plugin_text = "\n".join(plugin_list)
    await message.reply(f"**Installed Plugins:**\n```\n\n{plugin_text}```")

