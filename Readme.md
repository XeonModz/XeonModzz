<p align="center">
  <img src="https://files.catbox.moe/b34n8z.jpg" alt="XEON" width="700">
</p>

# XEON MODZ V1

A simple Telegram bot built using [Pyrogram](https://github.com/pyrogram/pyrogram) & [Pyrofrok](https://github.com/Mayuri-Chan/pyrofork), featuring basic command-line utilities.

## Features & Commands

### User Commands
- `/start` - Start the bot.
- `/alive` - Check bot status.
- `/menu` / `/help` / `/list` - Show available commands.
- `/id` - Get chat ID.
- `/ping` - Check bot latency.
- `/sysinfo` - Show system info.
- `/stats` - Show bot statistics.
- `/uptime` - Show bot uptime.
- `/insta` - Instagram downloader.
- `/teradl` - Terabox downloader.
- `/pin` - Pinterest downloader.
- `/upload` - Image uploader.
- `/fancy` - Fancy text generator.
- `/img` - Search images.
- `/pp` - Update profile picture.
- `/gpp` - Update group picture.
- `/url` - Convert image/video/audio to URL.
- `/fb` - Facebook downloader.
- `/ginfo` - Show the group profile picture with details.
- `/tagall` - Tag all members in group.
- `/removebg` - Remove background of image.
- `/antibot` - Remove all bots.
- `/antilink` - Remove all links.
- `/sticker` - Convert image to sticker.
- `/crop` - Crop image to PDF 512x512.
- `/unzip` - Unzip the zip/video.
- `/song` - Download YouTube music.

### Owner Commands (Requires Sudo Privileges)
- `/owner` - Show owner command list.
- `/eval <code>` - Evaluate Python expressions.
- `/reboot` - Restart the bot.
- `/shutdown` - Shutdown the bot.
- `/shell` / `/cmd` - Run shell commands.
- `/install` - Install plugins.
- `/uninstall` - Uninstall plugins.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/hrithikuday/XeonModzz.git
   cd XeonModzz
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure environment variables:
   - Create a `.env` file and add your API keys:
     ```env
     API_ID=your_api_id
     API_HASH=your_api_hash
     BOT_TOKEN=your_bot_token
     SUDO=0,0
     PORT=5000
     ```

## Usage
Run the bot with:
```sh
python3 -m xeonmodz
```

## Deployment
You can deploy the bot on:
- **Render**
- **Koyeb**
- **VPS/Dedicated Server**
- **Local Machine**

## Contributing
Feel free to fork and submit pull requests to improve the bot.

## License
This project is licensed under the General Public License. See `LICENSE` for details.

