# Version: 1.0 Beta
# ©️ 2025 DOTSERMODZ ALL RIGHTS RESERVED
from config import ROZE_API ,BOT_NAME ,CATBOX_API_URL
import os, instaloader, re, random, requests
from urllib.parse import urlparse, parse_qs ,quote_plus


# teradl
def sanitize_filename(filename):
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename) or f"{BOT_NAME}."

def terafetch_download_data(url):
    response = requests.get(ROZE_API+".teradl?url=" + url)
    if response.status_code != 200:
        return None
    return response.json()

def teradownload_file(download_link, file_path):
    with requests.get(download_link, stream=True) as file_response:
        if file_response.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in file_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
    return False

# instadl
L = instaloader.Instaloader()

def download_instagram_post(url):
    post_identifier = url.split("/")[-2]
    post = instaloader.Post.from_shortcode(L.context, post_identifier)
    L.download_post(post, target=post.profile)
    return post.profile


# catbox upload
def upload_to_catbox(file_path):
    files = {'fileToUpload': open(file_path, 'rb')}
    data = {'reqtype': 'fileupload'}
    response = requests.post(CATBOX_API_URL, files=files, data=data)
    return response.text.strip()


# wallpaper DL
def fetch_wallpapers(query):
    response = requests.get(ROZE_API +"/search?wallpaper=" + query)
    if response.status_code != 200:
        return None
    return response.json().get("wallpapers", [])

def select_random_wallpapers(wallpapers, count=10):
    return random.sample(wallpapers, min(count, len(wallpapers)))

async def send_wallpapers(client, message, wallpapers, query):
    for wallpaper in wallpapers:
        download_link = wallpaper.get("download_link")
        if download_link:
            await message.reply_document(document=download_link, caption=f"Wallpaper: {query}")
        else:
            await message.reply_text("Could not retrieve wallpaper link.")
# qr code
def fetch_qr(text):
    # Encode text safely for URLs
    encoded_text = quote_plus(text)
    api_url = f"{ROZE_API}/get_qr?text={encoded_text}"
    
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            file_path = f"qr_{encoded_text}.png"
            with open(file_path, "wb") as file:
                file.write(response.content)
            return file_path
    except Exception as e:
        print(f"[QR ERROR] {e}")
    return None


def qr_del(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

# Google Drive

def gdrive_extract_file_id(drive_link: str) -> str | None:
    if "drive.google.com" in drive_link:
        match = re.search(r"[-\w]{25,}", drive_link)
        return match.group(0) if match else None
    try:
        parsed_url = urlparse(drive_link)
        return parse_qs(parsed_url.query).get("id", [None])[0]
    except Exception:
        return None

def gdrive_get_file_info(download_url: str) -> tuple[str, int]:
    head = requests.head(download_url, allow_redirects=True)
    if 'content-length' not in head.headers:
        raise ValueError("Could not retrieve file info. Check the link!")
    content_length = int(head.headers["content-length"])
    if "content-disposition" in head.headers:
        disposition = head.headers["content-disposition"]
        filename_match = re.findall(r'filename="(.+)"', disposition)
        file_name = filename_match[0] if filename_match else "file"
    else:
        file_name = "file"
    return file_name, content_length

def gdrive_download_file(download_url: str, file_path: str):
    response = requests.get(download_url, stream=True)
    with open(file_path, "wb") as f:
        for chunk in response.iter_content(1024 * 1024):
            if chunk:
                f.write(chunk)
