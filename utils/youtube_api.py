from googleapiclient.discovery import build
from datetime import datetime, timedelta
from utils.config import Config
import re

YOUTUBE = build("youtube", "v3", developerKey=Config.YOUTUBE_API_KEY, cache_discovery=False)

def get_published_after_date():
    date_obj = datetime.utcnow() - timedelta(days=Config.PUBLISHED_AFTER_DAYS)
    return date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")

def fetch_video_details(video_ids):
    videos = []
    if not video_ids:
        return videos
    request = YOUTUBE.videos().list(
        part="snippet",
        id=",".join(video_ids)
    )
    response = request.execute()
    for item in response.get("items", []):
        snippet = item["snippet"]
        channel_id = snippet.get("channelId")
        videos.append({
            "id": item["id"],
            "title": snippet.get("title"),
            "description": snippet.get("description"),
            "channel": snippet.get("channelTitle"),
            "channel_id": channel_id,
            "link": f"https://www.youtube.com/watch?v={item['id']}",
            "type": "video",
            "publishedAt": snippet.get("publishedAt")
        })
    return videos

def fetch_video_details_sorted(video_ids):
    videos = []
    if not video_ids:
        return videos

    request = YOUTUBE.videos().list(
        part="snippet,statistics",  # Include statistics for view count
        id=",".join(video_ids)
    )
    response = request.execute()

    for item in response.get("items", []):
        snippet = item["snippet"]
        stats = item.get("statistics", {})
        channel_id = snippet.get("channelId")
        views = int(stats.get("viewCount", 0))

        videos.append({
            "id": item["id"],
            "title": snippet.get("title"),
            "description": snippet.get("description"),
            "channel": snippet.get("channelTitle"),
            "channel_id": channel_id,
            "link": f"https://www.youtube.com/watch?v={item['id']}",
            "type": "video",
            "publishedAt": snippet.get("publishedAt"),
            "views": views
        })

    # Sort videos by view count in descending order
    return sorted(videos, key=lambda v: v["views"], reverse=True)

def search_youtube_videos(query, max_results=20, order="relevance"):
    published_after = get_published_after_date()
    request = YOUTUBE.search().list(
        q=query,
        part="snippet",
        maxResults=max_results,
        type="video",
        regionCode=Config.REGION_CODE,
        safeSearch="moderate",
        relevanceLanguage="en",
        publishedAfter=published_after,
        order=order
    )
    response = request.execute()
    video_ids = [item["id"]["videoId"] for item in response.get("items", [])]

    if order != "viewCount":
        return fetch_video_details_sorted(video_ids), 100 + 2*len(video_ids)
    else:
        return fetch_video_details(video_ids), 100 + len(video_ids)
    
def fetch_related_videos(video_id, max_results=10):
    request = YOUTUBE.search().list(
        relatedToVideoId=video_id,
        part="snippet",
        type="video",
        maxResults=max_results,
        regionCode=Config.REGION_CODE,
        relevanceLanguage="en",
        safeSearch="moderate"
    )
    response = request.execute()
    related_ids = [item["id"]["videoId"] for item in response.get("items", [])]
    return fetch_video_details(related_ids)

def unified_youtube_search(query, max_results=10, order="relevance"):
    videos, quota = search_youtube_videos(query, max_results=max_results, order=order)
    return videos, quota
