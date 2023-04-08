import os
from dotenv import load_dotenv
import time
import datetime
import pytz
import feedparser
from main import update_database
import logging

load_dotenv()

# Set up logging
logging.basicConfig(
    filename='rss_monitor.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
)

RSS_FEED_URL = "https://feeds.noagendaassets.com/noagenda.xml"

def get_latest_entry(feed_url):
    feed = feedparser.parse(feed_url)
    if not feed.entries:
        return None
    return max(feed.entries, key=lambda entry: entry.published_parsed)

def main():
    last_entry = get_latest_entry(RSS_FEED_URL)
    if last_entry:
        logging.info(f"Latest entry: {last_entry.title}, published on {last_entry.published}")

    while True:
        try:
            latest_entry = get_latest_entry(RSS_FEED_URL)
            if latest_entry and latest_entry != last_entry:
                logging.info(f"New entry detected: {latest_entry.title}, published on {latest_entry.published}")
                last_entry = latest_entry

                # Run your script when a new entry is detected
                update_database()
            time.sleep(180)  # Check for updates every 180 seconds
        except Exception as e:
            logging.error(f"Error occurred while updating database: {e}")
            time.sleep(180)  # Wait a bit before trying again

if __name__ == "__main__":
    main()
