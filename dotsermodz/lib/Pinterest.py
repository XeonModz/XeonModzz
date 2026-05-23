# Version: 1.0 Beta
# ©️ 2025 DOTSERMODZ ALL RIGHTS RESERVED
import requests
import random

def generate_user_agent():
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Function to check if the URL is valid (basic check)
def is_url(url):
    return url.startswith("http://") or url.startswith("https://")

# Pinterest downloader function
async def pinterest(url):
    if not is_url(url):
        raise ValueError("Need Pinterest URL")

    headers = {
        "User-Agent": generate_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    }

    try:
        response = requests.get(f"https://pinterestdownloader.io/frontendService/DownloaderService?url={url}", headers=headers)
        response.raise_for_status()
        data = response.json()

        medias = data.get("medias", [])
        highest_quality_video = None
        highest_quality_image = None

        for media in medias:
            if media["extension"] == "mp4":
                if not highest_quality_video or media["quality"] > highest_quality_video["quality"]:
                    highest_quality_video = media
            elif media["extension"] in ["jpg", "png"]:
                if not highest_quality_image or media["quality"] > highest_quality_image["quality"]:
                    highest_quality_image = media

        if highest_quality_video:
            return highest_quality_video["url"]
        elif highest_quality_image:
            return highest_quality_image["url"]
        else:
            raise ValueError("No media found")
    except Exception as e:
        raise ValueError(f"Error fetching Pinterest media: {e}")


REMOVE_BG_KEYS = [
    "q61faXzzR5zNU6cvcrwtUkRU",
    "S258diZhcuFJooAtHTaPEn4T",
    "5LjfCVAp4vVNYiTjq9mXJWHF",
    "aT7ibfUsGSwFyjaPZ9eoJc61",
    "BY63t7Vx2tS68YZFY6AJ4HHF",
    "5Gdq1sSWSeyZzPMHqz7ENfi8",
    "86h6d6u4AXrst4BVMD9dzdGZ",
    "xp8pSDavAgfE5XScqXo9UKHF",
    "dWbCoCb3TacCP93imNEcPxcL"
]

def remove_background(image_path: str) -> tuple[bool, bytes | str]:
    """Try all API keys to remove background. Returns (success, content or error)."""
    for api_key in random.sample(REMOVE_BG_KEYS, len(REMOVE_BG_KEYS)):
        with open(image_path, 'rb') as img_file:
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': img_file},
                data={'size': 'auto'},
                headers={'X-Api-Key': api_key},
            )

        if response.status_code == requests.codes.ok:
            return True, response.content
        else:
            continue
    return False, f"{response.status_code} — {response.text}"


