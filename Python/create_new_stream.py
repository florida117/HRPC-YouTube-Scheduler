#!/usr/bin/env python3
"""
One-time script to create a new reusable YouTube live stream
and get the stream ID and stream key for OBS configuration.

Run this once, then update Morning_Service.py with the new stream_id.
"""

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

HOME = os.path.expanduser("~")

def authenticate(HOME):
    SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
    credentials_file = HOME + "/git/HRPC-YouTube-Scheduler/Python/token.pickle"

    if os.path.exists(credentials_file):
        with open(credentials_file, 'rb') as token:
            credentials = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            HOME + "/git/HRPC-YouTube-Scheduler/Python/client_secret.json", 
            scopes=SCOPES
        )
        credentials = flow.run_local_server(port=8080)
        with open(credentials_file, 'wb') as token:
            pickle.dump(credentials, token)
    return credentials

def create_youtube_client(credentials):
    return build('youtube', 'v3', credentials=credentials)

def create_reusable_stream(youtube):
    """Create a new reusable live stream"""
    request = youtube.liveStreams().insert(
        part="snippet,cdn,contentDetails,status",
        body={
            "snippet": {
                "title": "HRPC Reusable Livestream",
                "description": "Reusable stream for HRPC Sunday services"
            },
            "cdn": {
                "frameRate": "variable",
                "ingestionType": "rtmp",
                "resolution": "variable"
            },
            "contentDetails": {
                "isReusable": True
            }
        }
    )
    response = request.execute()
    return response

def main():
    print("=" * 60)
    print("Creating New Reusable YouTube Live Stream")
    print("=" * 60)
    
    # Authenticate
    credentials = authenticate(HOME)
    youtube = create_youtube_client(credentials)
    
    # Create the stream
    print("\nCreating stream...")
    stream_response = create_reusable_stream(youtube)
    
    # Extract the important details
    stream_id = stream_response['id']
    stream_name = stream_response['cdn']['ingestionInfo']['streamName']
    ingestion_address = stream_response['cdn']['ingestionInfo']['ingestionAddress']
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS! New stream created")
    print("=" * 60)
    
    print(f"\n📝 STREAM ID (use this in Morning_Service.py):")
    print(f"   {stream_id}")
    
    print(f"\n🔑 STREAM KEY (use this in OBS):")
    print(f"   {stream_name}")
    
    print(f"\n🌐 RTMP URL (use this in OBS):")
    print(f"   {ingestion_address}")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print(f"1. Update Morning_Service.py line ~203 to:")
    print(f'   stream_id = "{stream_id}"')
    print(f"\n2. Update your OBS Stream Settings:")
    print(f"   - Server: {ingestion_address}")
    print(f"   - Stream Key: {stream_name}")
    print("=" * 60)
    
    # Optionally save to file
    output_file = HOME + "/git/HRPC-YouTube-Scheduler/Service_Details/new_stream_info.txt"
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(f"Stream ID: {stream_id}\n")
            f.write(f"Stream Key: {stream_name}\n")
            f.write(f"RTMP URL: {ingestion_address}\n")
        print(f"\n💾 Stream info also saved to: {output_file}")
    except Exception as e:
        print(f"\n⚠️  Could not save to file: {e}")

if __name__ == "__main__":
    main()
