# Version: 1.0 Beta
# ©️ 2025 DOTSERMODZ ALL RIGHTS RESERVED
from pyrogram import Client, filters
from dotsermodz.lib.download import download_instagram_post,teradownload_file,sanitize_filename,terafetch_download_data ,fetch_wallpapers, select_random_wallpapers, send_wallpapers, gdrive_extract_file_id, gdrive_get_file_info, gdrive_download_file
from dotsermodz.lib import Pinterest
from pyrogram.types import Message
from dotsermodz.lib.mode import isPrivate
from dotsermodz import app 
import os


# Instagram Post Download
@app.on_message(filters.command("insta"))
@isPrivate
async def handle_instagram_post(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide an Instagram post URL.")
        return

    url = message.command[1]
    
    if "instagram.com" not in url:
        await message.reply_text("Only Instagram links are supported.")
        return

    if "stories" in url:
        await message.reply_text("Instagram stories links are not supported.")
        return

    try:
        profile_dir = download_instagram_post(url)

        # Send downloaded files, excluding .txt and .json.xz files
        downloaded_files = os.listdir(profile_dir)
        for filename in downloaded_files:
            if not (filename.endswith('.txt') or filename.endswith('.json.xz')):
                await message.reply_document(os.path.join(profile_dir, filename))
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")



# Pinterest Image Download
@app.on_message(filters.command("pinterest"))
@isPrivate
async def handle_pinterest(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a Pinterest URL.")
        return

    url = message.command[1]
    try:
        media_url = await Pinterest.pinterest(url)
        await message.reply_document(media_url, caption="Here is the media from the Pinterest Image")
    except Exception as e:
        await message.reply_text(str(e))

# Wallpaper Command

@app.on_message(filters.command("wallpaper"))
@isPrivate
async def wallpaper(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a search query. Example: /wallpaper nature")
        return

    query = " ".join(message.command[1:])
    wallpapers = fetch_wallpapers(query)

    if wallpapers is None:
        await message.reply_text("Failed to fetch wallpapers. Try again later.")
        return

    if not wallpapers:
        await message.reply_text("No wallpapers found for your query.")
        return

    random_wallpapers = select_random_wallpapers(wallpapers)
    await send_wallpapers(client, message, random_wallpapers, query)

# Teradl 
@app.on_message(filters.command("teradl"))
@isPrivate
async def teradl_handler(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a URL.\n\nExample: /teradl __Terabox url__")
        return
    
    url = message.command[1]
    data = terafetch_download_data(url)
    
    if not data:
        await message.reply_text("Failed to fetch download link.")
        return
    
    download_link = data.get("downloadLink")
    file_name = sanitize_filename(data.get("fileName", "Unknown_File"))
    file_format = data.get("fileName", "").split(".")[-1] if "." in data.get("fileName", "") else "mp4"
    
    if not download_link:
        await message.reply_text("Download link not found.")
        return
    
    os.makedirs("downloads", exist_ok=True)
    file_name = f"downloaded_file.{file_format}"
    file_path = os.path.join("downloads", file_name)
    
    if not teradownload_file(download_link, file_path):
        await message.reply_text("Failed to download file.")
        return
    
    await message.reply_document(file_path)
    os.remove(file_path)


# This function removes the background from an image using the remove.bg API.
@app.on_message(filters.command("rmbg"))
@isPrivate
async def remove_bg(client: Client, message: Message):
    
    if not message.reply_to_message:
        return await message.reply("Please reply to an image.")

    reply = message.reply_to_message

    if not reply.photo:
        return await message.reply("Please reply to an image.")

    msg = await message.reply("Downloading image...")

    photo_path = await client.download_media(reply.photo.file_id)

    await msg.edit("Removing background...")

    success, result = Pinterest.remove_background(photo_path)

    if success:
        output_path = "no-bg.png"
        with open(output_path, 'wb') as out:
            out.write(result)

        await msg.edit("Uploading no-background image...")
        await message.reply_document(output_path)
        os.remove(output_path)
    else:
        await msg.edit(f"❌ All keys failed.\n{result}")

    os.remove(photo_path)


# Google Drive Direct Link Download
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

@app.on_message(filters.command("gdrive"))
@isPrivate
async def gdirect_handler(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("❌ *Usage:* `/gdrive google_drive_direct_link`")

    drive_link = message.command[1].strip()
    await message.reply("*📥 Downloading file...*")

    file_id = gdrive_extract_file_id(drive_link)
    if not file_id:
        return await message.reply("❌ *Invalid Google Drive link or not a direct link!*")

    download_url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm=t"

    try:
        file_name, content_length = gdrive_get_file_info(download_url)
        
        if content_length is None:
            return await message.reply("❌ *Couldn't fetch file info. Possibly an invalid link.*")

        if content_length > MAX_FILE_SIZE:
            return await message.reply(
                f"❌ *File size exceeds 50MB limit!* (`{content_length / (1024 * 1024):.2f} MB`)"
            )

        if file_name == "file":
            file_name = f"file_{file_id}"

        file_size_mb = content_length / (1024 * 1024)
        file_path = f"/tmp/{file_name}"

        gdrive_download_file(download_url, file_path)

        caption = f"*{file_name}*\n\n*{file_size_mb:.2f} MB*\n\n⏤͟͟͞͞★❮DOTSERMODZ❯⏤͟͟͞͞★"
        await client.send_document(
            chat_id=message.chat.id,
            document=file_path,
            caption=caption,
            file_name=file_name
        )

        await message.reply("*✅ File sent successfully!*")
        os.remove(file_path)

    except Exception as e:
        print(f"Error: {e}")
        await message.reply("🚨 *An error occurred! Please check the link and try again.*")
