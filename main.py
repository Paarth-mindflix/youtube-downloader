import os
import json
import argparse 
from datetime import datetime
from utils.keyword_gen import generate_keywords
from utils.youtube_api import unified_youtube_search, fetch_related_videos
from utils.cache import CacheManager
from utils.manty_logger import CustomLogger
from utils.links_channel import fetch_video_links as fetch_channel_links
from utils.config import Config
from utils.s3_uploader import upload_file_to_s3
from collections import OrderedDict

# --- Setup ---
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_DIR = f"outputs/youtube_crawl_{timestamp}"
os.makedirs(OUTPUT_DIR, exist_ok=True)

log_file = "youtube_crawler.log"
logger = CustomLogger(log_file).get_logger()

cache = CacheManager()
quota_used = 0

def save_results(metadata, links, output_dir):

    metadata_output_file = os.path.join(output_dir, "video_metadata.json")
    with open(metadata_output_file, "w") as f:
        json.dump(metadata, f, indent=4)

    video_output_file = os.path.join(output_dir, "video_links.txt")
    with open(video_output_file, "w") as f:
        f.writelines(link + "\n" for link in links)

    #uploading the file to s3
    s3_key = f"experiment_{timestamp}/V_time_{timestamp}.txt"
    upload_file_to_s3(video_output_file, "youtubefiles3", s3_key, logger)
    
    #uploading the file to s3
    s3_key = f"experiment_{timestamp}/video_metadata.txt"
    upload_file_to_s3(metadata_output_file, "youtubefiles3", s3_key, logger)

def main(driver_path):
    global quota_used
    logger.info("Starting YouTube Indian Talking Face Crawler...")
    all_video_links = []
    all_metadata = []

    # ---------- STEP 1: Generate Keywords ----------
    keywords = generate_keywords(total=Config.KEYWORDS_PER_RUN, use_gpt=True)
    logger.info(f"Generated {len(keywords)} keywords.")
    logger.info(f"Keywords are {keywords}")

    # ---------- STEP 2: Iterate over keywords ----------
    for keyword in keywords:
        if cache.is_seen("seen_queries", keyword):
            logger.info(f"Skipping previously used keyword: {keyword}")
            continue

        # ---------- STEP 3: Iterate over order types ----------
        for order in Config.ORDERS:
            logger.info(f"Searching keyword '{keyword}' with order '{order}'")
            video_results, quota = unified_youtube_search(
                query=keyword,
                max_results=Config.MAX_RESULTS_PER_SEARCH,
                order=order
            )
            quota_used += quota

            # ---------- STEP 4: Deduplicate before selecting top K ----------
            unique_videos = {}
            for v in video_results:
                if v["type"] != "video":
                    continue
                vid = v["id"]
                # Keep highest view-count version if duplicate IDs appear
                if vid not in unique_videos or v.get("views", 0) > unique_videos[vid].get("views", 0):
                    unique_videos[vid] = v

            deduped_videos = list(unique_videos.values())

            # ---------- STEP 5: Filter unseen videos ----------
            top_videos = [
                v for v in deduped_videos
                if not cache.is_seen("seen_videos", v["id"])
            ]

            # ---------- STEP 6: Save all video links + metadata ----------
            for video in top_videos:
                all_video_links.append(video["link"])
                all_metadata.append(video)
                cache.mark_seen("seen_videos", video["id"])

            # ---------- STEP 7: Pick Top K unique channels from deduped list ----------
            selected_count = 0
            for video in top_videos:
                channel_id = video["channel_id"]
                if cache.is_seen("seen_channels", channel_id):
                    continue

                channel_file = os.path.join(OUTPUT_DIR, f"C_{channel_id}.txt")
                fetch_channel_links(
                    f"https://www.youtube.com/channel/{channel_id}/videos",
                    channel_file,
                    driver_path=driver_path,
                    max_videos=100
                )

                # Upload to S3
                s3_key = f"experiment_{timestamp}/C_{channel_id}.txt"
                upload_file_to_s3(channel_file, "youtubefiles3", s3_key, logger)
                cache.mark_seen("seen_channels", channel_id)

                selected_count += 1
                if selected_count >= Config.FILTER_TOP_K_FOR_RELATED:
                    break  # Only K unique channels per order

        cache.mark_seen("seen_queries", keyword)

    # ---------- STEP 8: Save metadata + links ----------
    save_results(all_metadata, all_video_links, OUTPUT_DIR)

    logger.info(f"Completed! Saved {len(all_video_links)} unique video links.")
    logger.info(f"Total YouTube quota units consumed: {quota_used}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch video links from a YouTube playlist."
    )
    parser.add_argument(
        "chrome_driver_path", type=str, help="The path of chromedriver.exe"
    )
    args = parser.parse_args()
    main(driver_path = args.chrome_driver_path)