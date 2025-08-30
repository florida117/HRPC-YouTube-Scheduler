# Upload_Sermon.py
import os, sys, base64, mimetypes, requests, subprocess

# Location of your secrets file
HOME = os.path.expanduser("~")
secrets_dir = os.path.join(HOME, "git", "HRPC-YouTube-Scheduler", "Python")
if secrets_dir not in sys.path:
    sys.path.insert(0, secrets_dir)

from log_in import secrets  # expects secrets['website_user_name'], secrets['website_password']

WORDPRESS_MEDIA_ENDPOINT = "https://www.hrpc.org.uk/wp-json/wp/v2/media"
NOTIFY = os.path.join(HOME, "hrpc_po.sh")  # push notification script

def send_notification(message: str):
    if os.path.isfile(NOTIFY) and os.access(NOTIFY, os.X_OK):
        subprocess.run([NOTIFY, message])
    else:
        print("⚠️ Notification script not found or not executable")

def upload_to_wordpress(file_path: str) -> str:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    username = secrets["website_user_name"]
    password = secrets["website_password"]

    credentials = f"{username}:{password}"
    token = base64.b64encode(credentials.encode()).decode("utf-8")

    filename = os.path.basename(file_path)
    mime, _ = mimetypes.guess_type(filename)
    if not mime:
        mime = "audio/mpeg"

    headers = {
        "Authorization": f"Basic {token}",
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-Type": mime,
    }

    with open(file_path, "rb") as f:
        r = requests.post(WORDPRESS_MEDIA_ENDPOINT, headers=headers, data=f)

    if r.status_code == 201:
        data = r.json()
        return data["source_url"]
    else:
        raise RuntimeError(f"Upload failed ({r.status_code}): {r.text}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Upload_Sermon.py <path_to_audio>", file=sys.stderr)
        sys.exit(2)
    file_path = sys.argv[1]

    try:
        url = upload_to_wordpress(file_path)
        msg = f"Sermon uploaded successfully:\n{os.path.basename(file_path)}\n{url}"
        print(msg)
        send_notification(msg)
        sys.exit(0)
    except Exception as e:
        err = f"Sermon upload FAILED:\n{os.path.basename(file_path)}\n{e}"
        print(err, file=sys.stderr)
        send_notification(err)
        sys.exit(1)