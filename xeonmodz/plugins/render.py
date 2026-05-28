from pyrogram import Client, filters
import requests
import os
from xeonmodz import app 
from config import RENDER_API_TOKEN,SUDO
import asyncio
from dotenv import load_dotenv
load_dotenv()
# Render API configuration

SERVICE_ID = os.environ.get("RENDER_SERVICE_ID")

RENDER_API_BASE = "https://api.render.com/v1/services"
HEADERS = {
    "Authorization": f"Bearer {RENDER_API_TOKEN}",
    "Content-Type": "application/json"
}

# /setvar VAR=VALUE
@app.on_message(filters.command("setvar")& filters.user(SUDO))
async def set_var(_, message):
    try:
        _, var_assignment = message.text.split(maxsplit=1)
        if '=' not in var_assignment:
            raise ValueError
        var_name, var_value = var_assignment.split("=", maxsplit=1)
    except ValueError:
        return await message.reply("Usage: `/setvar VAR=VALUE`", quote=True)

    url = f"{RENDER_API_BASE}/{SERVICE_ID}/env-vars/{var_name.strip()}"
    data = {"value": var_value.strip()}

    try:
        response = requests.put(url, headers=HEADERS, json=data)
        response.raise_for_status()

        # Trigger redeploy
        deploy_url = f"{RENDER_API_BASE}/{SERVICE_ID}/deploys"
        deploy_response = requests.post(deploy_url, headers=HEADERS)
        deploy_response.raise_for_status()

        await message.reply(f"✅ Set `{var_name}` to `{var_value}` and triggered redeploy.")
    except requests.exceptions.RequestException as e:
        error_msg = response.text if response is not None else str(e)
        await message.reply(f"❌ Failed to set variable or redeploy.\n```{error_msg}```")

# /delvar VAR_NAME

"""
@app.on_message(filters.command("delvar")& filters.user(SUDO))
async def del_var(_, message):
    try:
        _, var_name = message.text.split(maxsplit=1)
    except ValueError:
        return await message.reply("Usage: `/delvar VAR_NAME`", quote=True)

    url = f"{RENDER_API_BASE}/{SERVICE_ID}/env-vars/{var_name}"
    response = requests.delete(url, headers=HEADERS)

    

    if response.status_code == 204:
        await message.reply(f"🗑️ Deleted `{var_name}` successfully.")
    else:
        await message.reply(f"❌ Failed to delete `{var_name}`.\n```{response.text}```")
"""
@app.on_message(filters.command("delvar") & filters.user(SUDO))
async def del_var(_, message):
    try:
        _, var_name = message.text.split(maxsplit=1)
    except ValueError:
        return await message.reply("Usage: `/delvar VAR_NAME`", quote=True)

    url = f"{RENDER_API_BASE}/{SERVICE_ID}/env-vars/{var_name}"
    response = requests.delete(url, headers=HEADERS)

    if response.status_code == 204:
        await message.reply(f"🗑️ Deleted `{var_name}` successfully.")
        # Trigger redeploy
        redeploy_url = f"{RENDER_API_BASE}/{SERVICE_ID}/deploys"
        redeploy_response = requests.post(redeploy_url, headers=HEADERS)
        if redeploy_response.status_code == 201:
            await message.reply("🔁 Triggered redeploy successfully.")
        else:
            await message.reply(f"⚠️ Failed to trigger redeploy.\n```{redeploy_response.text}```")
    else:
        await message.reply(f"❌ Failed to delete `{var_name}`.\n```{response.text}```")
# /allvar


@app.on_message(filters.command("allenv")& filters.user(SUDO))
async def allvar(_, message):
    url = f'https://api.render.com/v1/services/{SERVICE_ID}/env-vars'
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {RENDER_API_TOKEN}',
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            text = ""

            if isinstance(data, list):
                for item in data:
                    env = item.get('envVar', {})
                    key = env.get('key')
                    value = env.get('value')
                    if key and value:
                        text += f"**{key}** = `{value}`\n"
                    else:
                        text += "⚠️ Missing 'key' or 'value' in one of the items.\n"
            else:
                text = f"Unexpected response format: `{data}`"

        else:
            text = f"❌ Failed to fetch env vars. Status: {response.status_code}\nResponse: `{response.text}`"

    except Exception as e:
        text = f"🚨 Error occurred: `{str(e)}`"

    await message.reply(text or "No environment variables found.", quote=True)

