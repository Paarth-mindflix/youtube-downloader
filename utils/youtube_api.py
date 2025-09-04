# # File: utils/youtube_api.py

# from googleapiclient.discovery import build
# from datetime import datetime, timedelta
# from utils.config import Config, REGION_CODE, PUBLISHED_AFTER_DAYS
# import re

# YOUTUBE = build("youtube", "v3", developerKey=Config.YOUTUBE_API_KEY, cache_discovery=False)

# def is_valid_video(item):
#     try:
#         duration = item.get("contentDetails", {}).get("duration", "")
#         match = re.match(r"PT(?:(\d+)M)?(?:(\d+)S)?", duration)
#         minutes = int(match.group(1) or 0)
#         seconds = int(match.group(2) or 0)
#         total_seconds = minutes * 60 + seconds
#         return total_seconds <= 1800  # 30s to 20min
#     except:
#         return False

# def get_published_after_date():
#     date_obj = datetime.utcnow() - timedelta(days=PUBLISHED_AFTER_DAYS)
#     return date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")

# def fetch_video_details(video_ids):
#     videos = []
#     if not video_ids:
#         return videos
#     request = YOUTUBE.videos().list(
#         part="snippet",
#         id=",".join(video_ids)
#     )
#     response = request.execute()
#     for item in response.get("items", []):
#         # if not is_valid_video(item):
#             # continue

#         snippet = item["snippet"]
#         channel_id = snippet.get("channelId")
#         videos.append({
#             "id": item["id"],
#             "title": snippet.get("title"),
#             "description": snippet.get("description"),
#             "channel": snippet.get("channelTitle"),
#             "channel_id": channel_id,
#             "link": f"https://www.youtube.com/watch?v={item['id']}",
#             "type": "video",
#             "publishedAt": snippet.get("publishedAt")
#         })
#     return videos


# def search_youtube_videos(query, max_results=20):
#     published_after = get_published_after_date()
#     request = YOUTUBE.search().list(
#         q=query,
#         part="snippet",
#         maxResults=max_results,
#         type="video",
#         regionCode=REGION_CODE,
#         safeSearch="moderate",
#         relevanceLanguage="en",
#         publishedAfter=published_after,
#         order="relevance"
#     )
#     response = request.execute()
#     video_ids = [item["id"]["videoId"] for item in response.get("items", [])]
#     quota = 100+(1*max_results)
#     return fetch_video_details(video_ids), quota

# def fetch_related_videos(video_id, max_results=10):
#     request = YOUTUBE.search().list(
#         relatedToVideoId=video_id,
#         part="snippet",
#         type="video",
#         maxResults=max_results,
#         regionCode=REGION_CODE,
#         relevanceLanguage="en",
#         safeSearch="moderate"
#     )
#     response = request.execute()
#     related_ids = [item["id"]["videoId"] for item in response.get("items", [])]
#     return fetch_video_details(related_ids)

# def search_youtube_channels(query, max_results=10):
#     request = YOUTUBE.search().list(
#         q=query,
#         part="snippet",
#         maxResults=max_results,
#         type="channel",
#         regionCode=REGION_CODE,
#         relevanceLanguage="en",
#         safeSearch="moderate"
#     )
#     response = request.execute()
#     results = []
#     for item in response.get("items", []):
#         channel_id = item["id"]["channelId"]
#         results.append({
#             "id": channel_id,
#             "title": item["snippet"]["title"],
#             "description": item["snippet"].get("description", ""),
#             "channel": item["snippet"]["channelTitle"],
#             "link": f"https://www.youtube.com/channel/{channel_id}/videos",
#             "type": "channel"
#         })
#     return results


# def search_youtube_playlists(query, max_results=10):
#     request = YOUTUBE.search().list(
#         q=query,
#         part="snippet",
#         maxResults=max_results,
#         type="playlist",
#         regionCode=REGION_CODE,
#         relevanceLanguage="en",
#         safeSearch="moderate"
#     )
#     response = request.execute()
#     results = []
#     for item in response.get("items", []):
#         playlist_id = item["id"]["playlistId"]
#         results.append({
#             "id": playlist_id,
#             "title": item["snippet"]["title"],
#             "description": item["snippet"].get("description", ""),
#             "channel": item["snippet"]["channelTitle"],
#             "link": f"https://www.youtube.com/playlist?list={playlist_id}",
#             "type": "playlist"
#         })
#     return results

# def unified_youtube_search(query, max_results_per_type=10):
#     total_quota = 0

#     # Videos
#     videos, quota = search_youtube_videos(query, max_results=max_results_per_type)
#     total_quota += quota  # search.list (video) costs 100 units

#     # Channels
#     channels = search_youtube_channels(query, max_results=max_results_per_type)
#     total_quota += 100  # search.list (channel) costs 100 units

#     # Playlists
#     playlists = search_youtube_playlists(query, max_results=max_results_per_type)
#     total_quota += 100  # search.list (playlist) costs 100 units

#     return videos + channels + playlists, total_quota

# if __name__ == "__main__":
#     related_videos = fetch_related_videos("https://www.youtube.com/watch?v=psEx5WRwjt0", max_results=5)
#     print(related_videos)





# youtube_api.py

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

    if order is not "viewCount":
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
