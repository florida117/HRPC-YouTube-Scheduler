import re
import requests
import os
from log_in import secrets
import subprocess

# Sets the location of the home folder
HOME = os.path.expanduser("~")
NOTIFY = os.path.join(HOME, "hrpc_po.sh")  # push notification script

def send_notification(message: str):
    if os.path.isfile(NOTIFY) and os.access(NOTIFY, os.X_OK):
        subprocess.run([NOTIFY, message])
    else:
        print("⚠️ Notification script not found or not executable")

# WordPress API credentials and endpoint
WP_URL = 'https://hrpc.org.uk/wp-json/wp/v2'
PAGE_ID = '8157'  # Replace with your page ID. For videos, 8157
USERNAME = secrets.get('website_user_name')
PASSWORD = secrets.get('website_password')

# Read the Good Friday service video ID from file
with open(HOME + '/git/HRPC-YouTube-Scheduler/Service_Details/good_friday_service_id.txt', 'r') as file:
    VIDEO_URL_1 = 'https://www.youtube.com/watch?v=' + file.read().strip()

# Second video slot is intentionally left blank for Good Friday
VIDEO_URL_2 = ''

# --- Step 1: Fetch the current page content ---
GET_RESPONSE = requests.get(
    f'{WP_URL}/pages/{PAGE_ID}?context=edit',
    auth=(USERNAME, PASSWORD)
)

if GET_RESPONSE.status_code != 200:
    MSG = f"Failed to fetch page: {GET_RESPONSE.status_code}"
    print(MSG)
    send_notification(MSG)
    exit(1)

# The REST API returns content as { "raw": "...", "rendered": "..." }.
# We need 'raw' so that shortcodes are preserved as-is.
PAGE_CONTENT = GET_RESPONSE.json()['content']['raw']

# --- Step 2: Replace the video URLs in the fetched content ---
# Matches [vc_video link="<anything up to the next quote>"]
# Group 1 captures the prefix including the opening quote so we can splice cleanly.
VC_VIDEO_PATTERN = r'(\[vc_video\s+link=")[^"]*'

matches = list(re.finditer(VC_VIDEO_PATTERN, PAGE_CONTENT))

if len(matches) < 2:
    MSG = f"Warning: expected 2 vc_video shortcodes, found {len(matches)}. Aborting update."
    print(MSG)
    send_notification(MSG)
    exit(1)

# Replace both: first gets the Good Friday video, second is set to blank
new_urls = [VIDEO_URL_1, VIDEO_URL_2]
for match, url in reversed(list(zip(matches[:2], new_urls))):
    PAGE_CONTENT = PAGE_CONTENT[:match.end(1)] + url + PAGE_CONTENT[match.end():]

# --- Step 3: POST the updated content back ---
DATA = {
    'content': PAGE_CONTENT
}

RESPONSE = requests.post(
    f'{WP_URL}/pages/{PAGE_ID}',
    json=DATA,
    auth=(USERNAME, PASSWORD)
)

# Check if the request was successful
if RESPONSE.status_code == 200:
    MSG = "Page updated successfully!"
    print(MSG)
    send_notification(MSG)
else:
    MSG = f"Failed to update page: {RESPONSE.status_code}"
    print(MSG)
    send_notification(MSG)
