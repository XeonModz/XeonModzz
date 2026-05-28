from xeonmodz.lib.base import get_os_uptime
from flask import Flask, render_template
import threading
from config import PORT
from datetime import datetime
import asyncio
import requests

flask_app = Flask(__name__)
start_time = datetime.now()


# for the web server
@flask_app.route('/')
def home():
    now = datetime.now()
    uptime = now - start_time
    os_uptime = get_os_uptime()
    return render_template('index.html', uptime=str(uptime).split('.')[0], start=start_time.strftime('%Y-%m-%d %H:%M:%S'), os_uptime=os_uptime)

def run_web():
    flask_app.run(host='0.0.0.0', port=PORT)

def yuji_itadori():
    server = threading.Thread(target=run_web, daemon=True)
    server.start()

# for the keep alive
# Only for render.com
async def luffy(host_url):
    while True:
        try:
            response = requests.get(host_url, timeout=50)
            print(f"\033[34mMonitor {host_url} for keep alive: {response.status_code}\033[0m")
        except requests.RequestException as e:
            print(f"\033[31mError pinging {host_url}: {e}\033[0m")
            
        await asyncio.sleep(5)