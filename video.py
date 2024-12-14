import os
from pyrogram import Client, filters
from yt_dlp import YoutubeDL
import asyncio 
from datetime import datetime
import time
#from config import *

def download_progress_hook(d):
    if d['status'] == 'downloading':
         print(f"Downloading {d['filename']}: {d['_percent_str']} at {d['_speed_str']} ETA {d['_eta_str']}")
    elif d['status'] == 'finished':
        print(f"Download complete: {d['filename']}")


def download_video(url, output_path='downloads'):
    try:
        with YoutubeDL({'skip_download': True, 'quiet': True, 'dump_single_json': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            ydl_opts = {
                'format': 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]',
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'external_downloader': 'aria2c',
                'external_downloader_args': ['-j', '16', '-x', '16', '-s', '16', '-k', '10M'],
                'playlistend': 100, 'writethumbnail': True, 'progress_hooks': [download_progress_hook],
            }
            print(f"Downloading... {url}")
            YoutubeDL(ydl_opts).download([url])
            print(f"Video downloaded successfully from URL: {url}")
    except Exception as e:
        print(f"Failed to download video from URL: {url}. Error: {e}")

def upload_progress(current, total):
    if current == total:
        print(f"Uploaded")

async def upload_video(app, chat_id, file_path, thumbnail_path):
    try:
        video = await app.send_video(chat_id, file_path, caption=file_path.split("/", 2)[-1], thumb=thumbnail_path, progress=upload_progress)
        print(f"Video {file_path.split('/', 2)[-1]} uploaded successfully to chat ID: {chat_id}")
        return video
    except Exception as e:
        print(f"Failed to upload video to chat ID: {chat_id}. Error: {e}")
