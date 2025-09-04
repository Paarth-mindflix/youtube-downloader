import os
import json

class CacheManager:
    def __init__(self, cache_dir=".cache"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cache = {}
        self._load_all()

    def _cache_path(self, key):
        return os.path.join(self.cache_dir, f"{key}.json")

    def _load_all(self):
        for key in ["seen_queries", "seen_videos", "seen_channels", "seen_playlists"]:
            path = self._cache_path(key)
            if os.path.exists(path):
                with open(path, "r") as f:
                    self.cache[key] = set(json.load(f))
            else:
                self.cache[key] = set()

    def is_seen(self, key, item):
        return item in self.cache.get(key, set())

    def mark_seen(self, key, item):
        self.cache.setdefault(key, set()).add(item)
        self._save(key)

    def _save(self, key):
        path = self._cache_path(key)
        with open(path, "w") as f:
            json.dump(list(self.cache[key]), f, indent=2)
