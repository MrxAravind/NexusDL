import requests
import os
import logging
from pyrogram import Client, filters
import asyncio 
from datetime import datetime
import time
from config import *
from database import *
from video import *
import static_ffmpeg



# Configure logging
logging.basicConfig(
    filename='NexusDL.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

db = connect_to_mongodb(DATABASE_URL, "Spidydb")
collection_name = "NexusDL"



# Create the Pyrogram client
app = Client("SpidyPHVDL", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN,workers=100)


static_ffmpeg.add_paths()



def get_data():
    try:
        url = "https://stupidfucker79.github.io/Shiny-Scarper/links.txt"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.text.split("\n\n")
            return [i.strip() for i in data]
        else:
            return f"Error: Received status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"





async def main():
        logging.info("Bot Started")
        video_urls = []
        video_urls = get_data()
        print(video_urls)
        uploading = []
        for video_url in video_urls:
            video_hash = hash(video_url)
            download_dir = f'downloads/{video_hash}'
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
            try:
                downloaded_video_path = download_video(video_url, output_path=download_dir)
                exact_file_path = None
                thumbnail_path = None
                title = data[video_urls.index(video_url)][0]
                for root, dirs, files in os.walk(download_dir):
                    for file in files:
                        if file.endswith(('.mp4', '.mkv', '.webm')):
                            exact_file_path = os.path.join(root, file)
                        if exact_file_path and exact_file_path.split("/", 2)[-1] not in [uploads[0] for uploads in uploading]:
                                        uploading.append([exact_file_path.split("/", 2)[-1],video_url])
                                        video = await upload_video(app, DUMP_ID, exact_file_path)
                                        result = {
                                            "URL": video_url,
                                            "File_Name": exact_file_path.split("/", 2)[-1],
                                            "CHAT_ID": DRIVE_ID,    
                                         }
                                        insert_document(db, table_name, result)
                                        os.remove(exact_file_path)
                                        os.remove(thumbnail_path)
                else:
                    logging.error(f"Downloaded video or thumbnail file not found in '{download_dir}' directory.")
            except Exception as e:
                logging.error(f"An error occurred: {e}")

asyncio.run(main())
