from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import argparse

# Configure logging
from .manty_logger import CustomLogger
log_file = "youtube_extractor.log"
logger = CustomLogger(log_file).get_logger()

def fetch_playlist_links(playlist_url, output_file, max_videos=300):
    # Path to your WebDriver (update this with your WebDriver path)
    driver_path = "C:/Windows/System32/chromedriver.exe"  # Replace with the path to your WebDriver
    service = Service(driver_path)

    # Set up the WebDriver
    driver = webdriver.Chrome(service=service)

    try:
        # Open the YouTube playlist page
        driver.get(playlist_url)
        time.sleep(10)  # Allow the page to load

        # Scroll down to load all videos in the playlist
        video_links = set()  # Use a set to avoid duplicates
        scroll_pause_time = 10
        last_height = driver.execute_script(
            "return document.documentElement.scrollHeight"
        )

        while len(video_links) < max_videos:
            # Find all video links on the playlist page
            elements = driver.find_elements(By.XPATH, '//a[@id="video-title"]')
            for elem in elements:
                href = elem.get_attribute("href")
                if href and "/watch?v=" in href:
                    video_links.add(href)

            # Break if we've collected enough links
            if len(video_links) >= max_videos:
                break

            # Scroll down and wait for the page to load new content
            driver.execute_script(
                "window.scrollTo(0, document.documentElement.scrollHeight);"
            )
            time.sleep(scroll_pause_time)

            # Check if the page has stopped loading new content
            new_height = driver.execute_script(
                "return document.documentElement.scrollHeight"
            )
            if new_height == last_height:
                logger.info("No more content to load.")
                break
            last_height = new_height

        # Save the video links to the output file
        with open(output_file, "a") as file:
            file.writelines(link + "\n" for link in list(video_links)[:max_videos])

        logger.info(f"Saved {len(video_links)} video links to {output_file}")

    except Exception as e:
        logger.info(f"An error occurred: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Fetch video links from a YouTube playlist."
    )
    parser.add_argument(
        "playlist_url", type=str, help="The URL of the YouTube playlist."
    )
    parser.add_argument(
        "output_file", type=str, help="The file to save the video links."
    )
    parser.add_argument(
        "--max_videos",
        type=int,
        default=300,
        help="The maximum number of video links to fetch.",
    )

    args = parser.parse_args()

    # Fetch and save video links
    fetch_playlist_links(args.playlist_url, args.output_file, args.max_videos)
