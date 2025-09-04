import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from the .env file
env_path = Path(".") / ".env"
load_dotenv()

class Config:
    """Manages Environment, API Keys, and Secrets"""

    ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
    USE_PROXY = ENVIRONMENT == "prod"

    # API Keys
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")

    @staticmethod
    def check_env_vars():
        required_vars = ["YOUTUBE_API_KEY", "OPENAI_API_KEY"]
        for var in required_vars:
            if not os.getenv(var):
                raise Exception(f"Missing required environment variable: {var}")

    # --- YouTube Configuration ---
    MAX_RESULTS_PER_SEARCH = 50                 # maxResults per video search
    MAX_RESULTS_RELATED = 20                    # maxResults per related video call
    FILTER_TOP_K_FOR_RELATED = 5                # filter top N videos for related search
    ORDERS = ["relevance", "viewCount"]        # order types per keyword
    KEYWORDS_PER_RUN = 16                      # total keywords to generate
    REGION_CODE = "IN"
    PUBLISHED_AFTER_DAYS = 270

    # --- Quota Costs ---
    QUOTA_COST_SEARCH_LIST = 100               # per search.list call
    QUOTA_COST_VIDEOS_LIST = 2                 # per video ID
    QUOTA_COST_RELATED_SEARCH = 100            # for relatedToVideoId call

    # --- Output ---
    SQLITE_DB_PATH = "youtube_cache.db"
    OUTPUT_BUCKET = "youtubefiles3"

# Ensure required variables are present
Config.check_env_vars()

