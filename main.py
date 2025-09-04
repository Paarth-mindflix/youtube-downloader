# # File: main.py

# import os
# import json
# from datetime import datetime
# from utils.keyword_gen import generate_keywords
# from utils.youtube_api import search_youtube_videos, fetch_related_videos
# from utils.cache import CacheManager
# from utils.manty_logger import CustomLogger
# from utils.links_channel import fetch_video_links as fetch_channel_links
# from utils.links_playlist import fetch_playlist_links

# # --- Setup ---
# timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# OUTPUT_DIR = f"outputs/youtube_crawl_{timestamp}"
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# log_file = "youtube_crawler.log"
# logger = CustomLogger(log_file).get_logger()

# cache = CacheManager()


# def save_results(metadata, links, output_dir):
#     with open(os.path.join(output_dir, "video_metadata.json"), "w") as f:
#         json.dump(metadata, f, indent=4)
#     with open(os.path.join(output_dir, "video_links.txt"), "w") as f:
#         f.writelines(link + "\n" for link in links)


# def main():
#     logger.info("Starting YouTube Indian Talking Face Crawler...")
#     all_video_links = []
#     all_metadata = []

#     keywords = generate_keywords(total=40, use_gpt=True)
#     logger.info(f"Generated {len(keywords)} keywords.")

#     for keyword in keywords:
#         if cache.is_seen("seen_queries", keyword):
#             logger.info(f"Skipping previously used keyword: {keyword}")
#             continue

#         logger.info(f"Searching videos for keyword: {keyword}")
#         video_results = search_youtube_videos(query=keyword, max_results=20)
#         logger.info(f"Found {len(video_results)} results for keyword '{keyword}'")

#         for video in video_results:
#             if cache.is_seen("seen_videos", video["id"]):
#                 continue

#             all_video_links.append(video["link"])
#             all_metadata.append(video)
#             cache.mark_seen("seen_videos", video["id"])

#             related_videos = fetch_related_videos(video_id=video["id"], max_results=10)
#             for rel_video in related_videos:
#                 if not cache.is_seen("seen_videos", rel_video["id"]):
#                     all_video_links.append(rel_video["link"])
#                     all_metadata.append(rel_video)
#                     cache.mark_seen("seen_videos", rel_video["id"])

#         cache.mark_seen("seen_queries", keyword)

#     # Fetch from discovered channels
#     for item in all_metadata:
#         if item["type"] == "channel" and not cache.is_seen("seen_channels", item["channel_id"]):
#             channel_file = os.path.join(OUTPUT_DIR, f"C_{item['channel_id']}.txt")
#             fetch_channel_links(item["link"], channel_file, max_videos=300)
#             cache.mark_seen("seen_channels", item["channel_id"])

#         if item["type"] == "playlist" and not cache.is_seen("seen_channels", item["id"]):
#             playlist_file = os.path.join(OUTPUT_DIR, f"P_{item['id']}.txt")
#             fetch_playlist_links(item["link"], playlist_file, max_videos=300)
#             cache.mark_seen("seen_channels", item["id"])

#     save_results(all_metadata, all_video_links, OUTPUT_DIR)

#     logger.info(f"Completed! Saved {len(all_video_links)} unique video links.")


# if __name__ == "__main__":
#     main()



# # File: main.py

# import os
# import json
# from datetime import datetime
# from utils.keyword_gen import generate_keywords
# from utils.youtube_api import unified_youtube_search, fetch_related_videos
# from utils.cache import CacheManager
# from utils.manty_logger import CustomLogger
# from utils.links_channel import fetch_video_links as fetch_channel_links
# from utils.links_playlist import fetch_playlist_links

# # --- Setup ---
# timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# OUTPUT_DIR = f"outputs/youtube_crawl_{timestamp}"
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# log_file = "youtube_crawler.log"
# logger = CustomLogger(log_file).get_logger()

# cache = CacheManager()
# quota_used = 0

# def save_results(metadata, links, output_dir):
#     with open(os.path.join(output_dir, "video_metadata.json"), "w") as f:
#         json.dump(metadata, f, indent=4)
#     with open(os.path.join(output_dir, "video_links.txt"), "w") as f:
#         f.writelines(link + "\n" for link in links)

# def main():
#     global quota_used
#     logger.info("Starting YouTube Indian Talking Face Crawler...")
#     all_video_links = []
#     all_metadata = []

#     keywords = generate_keywords(total=10, use_gpt=True)
#     logger.info(f"Generated {len(keywords)} keywords.")

#     for keyword in keywords:
#         if cache.is_seen("seen_queries", keyword):
#             logger.info(f"Skipping previously used keyword: {keyword}")
#             continue

#         logger.info(f"Searching content for keyword: {keyword}")
#         results, quota = unified_youtube_search(query=keyword)
#         quota_used += quota
#         logger.info(f"Quota used for keyword '{keyword}': {quota} units")

#         for item in results:
#             if item["type"] == "video" and not cache.is_seen("seen_videos", item["id"]):
#                 all_video_links.append(item["link"])
#                 all_metadata.append(item)
#                 cache.mark_seen("seen_videos", item["id"])

#                 # Fetch related videos for each video
#                 # related_videos = fetch_related_videos(video_id=item["id"], max_results=5)
#                 # quota_used += 100  # Each related video search counts as 100 units
#                 # for rel_video in related_videos:
#                 #     if not cache.is_seen("seen_videos", rel_video["id"]):
#                 #         all_video_links.append(rel_video["link"])
#                 #         all_metadata.append(rel_video)
#                 #         cache.mark_seen("seen_videos", rel_video["id"])

#             elif item["type"] == "channel" and not cache.is_seen("seen_channels", item["id"]):
#                 channel_file = os.path.join(OUTPUT_DIR, f"C_{item['id']}.txt")
#                 fetch_channel_links(item["link"], channel_file, max_videos=300)
#                 cache.mark_seen("seen_channels", item["id"])

#             elif item["type"] == "playlist" and not cache.is_seen("seen_playlists", item["id"]):
#                 playlist_file = os.path.join(OUTPUT_DIR, f"P_{item['id']}.txt")
#                 fetch_playlist_links(item["link"], playlist_file, max_videos=300)
#                 cache.mark_seen("seen_playlists", item["id"])

#         cache.mark_seen("seen_queries", keyword)

#     save_results(all_metadata, all_video_links, OUTPUT_DIR)

#     logger.info(f"Completed! Saved {len(all_video_links)} unique video links.")
#     logger.info(f"Total YouTube quota units consumed: {quota_used}")

# if __name__ == "__main__":
#     main()






# main.py

import os
import json
from datetime import datetime
from utils.keyword_gen import generate_keywords
from utils.youtube_api import unified_youtube_search, fetch_related_videos
from utils.cache import CacheManager
from utils.manty_logger import CustomLogger
from utils.links_channel import fetch_video_links as fetch_channel_links
from utils.links_playlist import fetch_playlist_links
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
    upload_file_to_s3(video_output_file, "youtubefiles3", s3_key)
    
    #uploading the file to s3
    s3_key = f"experiment_{timestamp}/video_metadata.txt"
    upload_file_to_s3(metadata_output_file, "youtubefiles3", s3_key)


def get_top_videos_across_orders(query, orders=["relevance", "viewCount"], max_results=50):
    all_videos = []
    total_quota = 0

    for order in orders:
        vids, quota = unified_youtube_search(query, max_results=Config.MAX_RESULTS_PER_SEARCH, order=order)
        all_videos.extend(vids)  # videos already contain 'views'
        total_quota+=quota

    # Deduplicate by ID while keeping the highest view count entry
    unique_videos = {}
    for v in all_videos:
        vid = v["id"]
        if vid not in unique_videos or v["views"] > unique_videos[vid]["views"]:
            unique_videos[vid] = v

    # Sort by view count descending
    sorted_videos = sorted(unique_videos.values(), key=lambda x: x["views"], reverse=True)

    return sorted_videos, total_quota  # Return all, or top-N later


def main():
    global quota_used
    logger.info("Starting YouTube Indian Talking Face Crawler...")
    all_video_links = []
    all_metadata = []

    keywords = generate_keywords(total=Config.KEYWORDS_PER_RUN, use_gpt=True)
    logger.info(f"Generated {len(keywords)} keywords.")
    logger.info(f"Keywords are {keywords}")

    for keyword in keywords:
        if cache.is_seen("seen_queries", keyword):
            logger.info(f"Skipping previously used keyword: {keyword}")
            continue

        for order in Config.ORDERS:
            logger.info(f"Searching keyword '{keyword}' with order '{order}'")
            video_results, quota = unified_youtube_search(
                query=keyword,
                max_results=Config.MAX_RESULTS_PER_SEARCH,
                order=order
            )
            quota_used += quota

            top_videos = [v for v in video_results if v["type"] == "video" and not cache.is_seen("seen_videos", v["id"])]

            for video in top_videos:
                all_video_links.append(video["link"])
                all_metadata.append(video)
                cache.mark_seen("seen_videos", video["id"])

            for video in top_videos[:Config.FILTER_TOP_K_FOR_RELATED]:
                if not cache.is_seen("seen_channels", video["channel_id"]):
                    channel_file = os.path.join(OUTPUT_DIR, f"C_{video['channel_id']}.txt")
                    fetch_channel_links(f"https://www.youtube.com/channel/{video['channel_id']}/videos", channel_file, max_videos=100)

                    #uploading the file to s3
                    s3_key = f"experiment_{timestamp}/C_{video['channel_id']}.txt"
                    upload_file_to_s3(channel_file, "youtubefiles3", s3_key)
                    cache.mark_seen("seen_channels", video["channel_id"])                

        cache.mark_seen("seen_queries", keyword)




    # for keyword in keywords:
    #     logger.info(f"Searching videos for keyword: {keyword}")
        
    #     all_results, quota = get_top_videos_across_orders(query=keyword, orders=Config.ORDERS)
    #     quota_used += quota

    #     top_videos_for_related = all_results[Config.FILTER_TOP_K_FOR_RELATED]  # 👈 Only use these for related search

    #     for video in all_results:
    #         if not cache.is_seen("seen_videos", video["id"]):
    #             all_video_links.append(video["link"])
    #             all_metadata.append(video)
    #             cache.mark_seen("seen_videos", video["id"])

    #     for top_video in top_videos_for_related:
    #         related_videos = fetch_related_videos(top_video["id"], max_results=Config.MAX_RESULTS_RELATED)
    #         quota_used+=quota

    #         for rel_video in related_videos:
    #             if not cache.is_seen("seen_videos", rel_video["id"]):
    #                 all_video_links.append(rel_video["link"])
    #                 all_metadata.append(rel_video)
    #                 cache.mark_seen("seen_videos", rel_video["id"])

    #     cache.mark_seen("seen_queries", keyword)


    save_results(all_metadata, all_video_links, OUTPUT_DIR)

    logger.info(f"Completed! Saved {len(all_video_links)} unique video links.")
    logger.info(f"Total YouTube quota units consumed: {quota_used}")

if __name__ == "__main__":
    main()