"""
Estimate total YouTube API quota usage and total videos collected
for the current hybrid pipeline (API + Selenium-based channel crawl).

Author: Manty (Paarth Dwivedi)
"""

from utils.config import Config

def estimate_quota_hybrid():
    """
    Estimates:
    1. API quota usage (search.list + videos.list)
    2. Total videos collected (API + Selenium crawls)
    """

    # ---- Core Configs ----
    keywords = Config.KEYWORDS_PER_RUN
    orders = Config.ORDERS
    max_results = Config.MAX_RESULTS_PER_SEARCH
    top_k_for_channels = Config.FILTER_TOP_K_FOR_RELATED   # Top K videos per keyword used for channel crawl
    max_videos_per_channel = 100                           # Matches main.py hardcoded value

    # ---- YouTube API Cost Assumptions ----
    # search.list → 100 units
    # videos.list (details fetch) → 1 unit per video
    SEARCH_LIST_COST = getattr(Config, "QUOTA_COST_SEARCH_LIST", 100)
    VIDEOS_LIST_COST = getattr(Config, "QUOTA_COST_VIDEOS_LIST", 1)

    # -------------------------------------
    # 1️⃣ Estimate API quota usage
    # -------------------------------------
    quota_per_keyword = 0

    for order in orders:
        # One search.list per keyword/order
        quota_per_keyword += SEARCH_LIST_COST
        # videos.list for details of each result
        quota_per_keyword += max_results * VIDEOS_LIST_COST

    total_quota_usage = quota_per_keyword * keywords

    # -------------------------------------
    # 2️⃣ Estimate number of videos collected
    # -------------------------------------
    # API results
    videos_from_api = keywords * len(orders) * max_results

    # Selenium channel crawls (no quota, just compute)
    videos_from_channels = keywords * top_k_for_channels * max_videos_per_channel

    total_videos_collected = videos_from_api + videos_from_channels

    # -------------------------------------
    # 3️⃣ Print Results
    # -------------------------------------
    print("===============================================")
    print("📊 YOUTUBE CRAWLER QUOTA & VIDEO ESTIMATOR")
    print("===============================================")
    print(f"Keywords per run           : {keywords}")
    print(f"Orders per keyword          : {orders}")
    print(f"Videos per API search       : {max_results}")
    print(f"Top-K channels per keyword  : {top_k_for_channels}")
    print(f"Videos per channel (Selenium): {max_videos_per_channel}")
    print("-----------------------------------------------")
    print(f"Estimated API quota usage   : {total_quota_usage} units")
    print(f"Estimated API videos        : {videos_from_api} videos")
    print(f"Estimated Selenium videos   : {videos_from_channels} videos")
    print("-----------------------------------------------")
    print(f"✅ Total videos (combined)  : {total_videos_collected}")
    print(f"⚡ Only API portion consumes quota; Selenium is free.")
    print("===============================================")


if __name__ == "__main__":
    estimate_quota_hybrid()
