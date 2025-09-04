from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import argparse

# Configure logging
from utils.manty_logger import CustomLogger
log_file = "youtube_extractor.log"
logger = CustomLogger(log_file).get_logger()

def fetch_video_links(channel_url, output_file, max_videos=300):
    # Path to your WebDriver (update with your actual path)
    driver_path = "C:/Windows/System32/chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(channel_url)
        time.sleep(10)  # Allow page to load

        video_links = set()
        scroll_pause_time = 10
        last_height = driver.execute_script("return document.documentElement.scrollHeight")

        while len(video_links) < max_videos:
            elements = driver.find_elements(By.XPATH, '//a[@id="thumbnail"]')
            for elem in elements:
                href = elem.get_attribute("href")
                if href and "/watch?v=" in href:
                    video_links.add(href)

            if len(video_links) >= max_videos:
                break

            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        with open(output_file, "w") as file:
            file.writelines(link + "\n" for link in list(video_links)[:max_videos])

    except Exception as e:
        logger.error(f"Error in fetch_video_links: {e}")
    finally:
        driver.quit()


def fetch_shorts_links(channel_url, output_file, max_shorts=300):
    """
    Fetch shorts links from the given channel's shorts page.
    Expects channel_url to be the URL for the shorts section (e.g., 
    "https://www.youtube.com/channel/{channel_id}/shorts")
    """
    driver_path = "C:/Windows/System32/chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(channel_url)
        time.sleep(10)  # Allow page to load

        shorts_links = set()
        scroll_pause_time = 10
        last_height = driver.execute_script("return document.documentElement.scrollHeight")

        while len(shorts_links) < max_shorts:
            # Use an XPath that looks for any anchor with "/shorts/" in its href.
            elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/shorts/")]')
            logger.debug(f"Found {len(elements)} elements on the page.")
            for elem in elements:
                href = elem.get_attribute("href")
                if href and "/shorts/" in href:
                    shorts_links.add(href)

            if len(shorts_links) >= max_shorts:
                break

            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        logger.debug(f"Total shorts found: {len(shorts_links)}")
        with open(output_file, "w") as file:
            file.writelines(link + "\n" for link in list(shorts_links)[:max_shorts])

    except Exception as e:
        logger.error(f"Error in fetch_shorts_links: {e}")
    finally:
        driver.quit()



def fetch_podcasts_links(channel_url, output_file, max_podcasts=300):
    """
    Fetch podcasts links from the given channel's podcasts page.
    Expects channel_url to be the URL for the podcasts section (e.g.,
    "https://www.youtube.com/channel/{channel_id}/podcasts")
    """
    driver_path = "C:/Windows/System32/chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(channel_url)
        time.sleep(10)  # Allow page to load

        podcasts_links = set()
        scroll_pause_time = 10
        last_height = driver.execute_script("return document.documentElement.scrollHeight")

        while len(podcasts_links) < max_podcasts:
            elements = driver.find_elements(By.XPATH, '//a[@id="thumbnail"]')
            for elem in elements:
                href = elem.get_attribute("href")
                if href and "/podcasts/" in href:
                    podcasts_links.add(href)

            if len(podcasts_links) >= max_podcasts:
                break

            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        with open(output_file, "w") as file:
            file.writelines(link + "\n" for link in list(podcasts_links)[:max_podcasts])

    except Exception as e:
        logger.error(f"Error in fetch_podcasts_links: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch video, shorts, or podcasts links from a YouTube channel section."
    )
    parser.add_argument("channel_url", type=str, help="The URL of the YouTube channel section.")
    parser.add_argument("output_file", type=str, help="The file to save the links.")
    parser.add_argument("--max_links", type=int, default=300, help="Maximum number of links to fetch.")
    parser.add_argument(
        "--section",
        type=str,
        choices=["videos", "shorts", "podcasts"],
        default="videos",
        help="Which section to scrape: videos, shorts, or podcasts.",
    )

    args = parser.parse_args()

    if args.section == "videos":
        fetch_video_links(args.channel_url, args.output_file, args.max_links)
    elif args.section == "shorts":
        fetch_shorts_links(args.channel_url, args.output_file, args.max_links)
    elif args.section == "podcasts":
        fetch_podcasts_links(args.channel_url, args.output_file, args.max_links)
