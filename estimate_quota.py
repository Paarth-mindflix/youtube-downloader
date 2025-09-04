from utils.config import Config

def estimate_quota():
    keywords = Config.KEYWORDS_PER_RUN
    orders = Config.ORDERS
    max_results = Config.MAX_RESULTS_PER_SEARCH
    top_k_for_related = Config.FILTER_TOP_K_FOR_RELATED
    related_results = Config.MAX_RESULTS_RELATED

    quota_per_keyword = 0

    # Each keyword x order → one search.list call (video) + videos.list
    for order in orders:
        quota_per_keyword += Config.QUOTA_COST_SEARCH_LIST  # search.list
        if order == "viewCount":
            quota_per_keyword += max_results * 1  # videos.list
        else:    
            quota_per_keyword += max_results * 1  # videos.list

        # Related video search on top K from each order
        # quota_per_keyword += top_k_for_related * Config.QUOTA_COST_RELATED_SEARCH
        # quota_per_keyword += top_k_for_related * related_results * 1

    total_quota = quota_per_keyword * keywords

    # Estimate video counts
    videos_per_keyword_order = (
        max_results + 100*Config.FILTER_TOP_K_FOR_RELATED
    )
    total_videos = videos_per_keyword_order * len(orders) * keywords

    print("------- Quota Usage Estimate -------")
    print(f"Keywords: {keywords}")
    print(f"Orders per keyword: {orders}")
    print(f"Videos per search: {max_results}")
    print("-------------------------------------")
    print(f"Estimated total quota usage: {total_quota} units")
    print(f"Estimated videos collected: {total_videos} videos")
    print("-------------------------------------")

def estimate_quota_optimised():
    keywords = Config.KEYWORDS_PER_RUN
    orders = Config.ORDERS
    max_results = Config.MAX_RESULTS_PER_SEARCH
    top_k_for_related = Config.FILTER_TOP_K_FOR_RELATED
    related_results = Config.MAX_RESULTS_RELATED

    quota_per_keyword = 0

    # --- 1. Search + Detail fetch ---
    for order in orders:
        quota_per_keyword += Config.QUOTA_COST_SEARCH_LIST  # search.list
        if order == "viewCount":
            quota_per_keyword += max_results * 1  # videos.list
        else:    
            quota_per_keyword += max_results * Config.QUOTA_COST_VIDEOS_LIST  # videos.list

    # --- 2. Related video search only for top-K combined videos ---
    quota_per_keyword += top_k_for_related * Config.QUOTA_COST_RELATED_SEARCH  # related search.list
    quota_per_keyword += top_k_for_related * related_results * 1  # details for related videos

    total_quota = quota_per_keyword * keywords

    # --- Video estimate ---
    videos_from_main = max_results * len(orders)
    videos_from_related = top_k_for_related * related_results
    total_videos = (videos_from_main + videos_from_related) * keywords

    print("------- Quota Usage Estimate for Optimised -------")
    print(f"Keywords: {keywords}")
    print(f"Orders per keyword: {orders}")
    print(f"Videos per search: {max_results}")
    print(f"Top {top_k_for_related} videos (globally) → related search")
    print(f"Related video results per video: {related_results}")
    print("-------------------------------------")
    print(f"Estimated total quota usage: {total_quota} units")
    print(f"Estimated videos collected: {total_videos} videos")
    print("-------------------------------------")

if __name__ == "__main__":
    estimate_quota()
    # estimate_quota_optimised()
