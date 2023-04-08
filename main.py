import asyncio
from db import add_credit, add_episode, last_episode_saved
from extractor import extractor, newest_episode

import os
from dotenv import load_dotenv

import sys
import warnings

if sys.platform.startswith('win'):
    if sys.version_info >= (3, 8) and sys.version_info < (3, 9):
        warnings.filterwarnings("ignore", category=ResourceWarning, message=".*Event loop is closed.*")

load_dotenv()

async def process_episode(episode_num=None):
    if episode_num is None:
        episode_num = int(await last_episode_saved()) + 1

    html = await extractor(episode_num)

    episode_date = html["epDate"]
    episode_title = html["epTitle"]
    episode_length = html["epLength"]
    episode_artist = html["epArtist"]
    executive_producers = html["epExecs"]
    associate_producers = html["epAssocs"]

    print(f"======== Start processing episode {episode_num} ========")

    for producer in executive_producers:
        credit = {
            "producer": producer,
            "type": "Executive",
            "episode_number": episode_num,
        }
        await add_credit(credit)

    for producer in associate_producers:
        credit = {
            "producer": producer,
            "type": "Associate",
            "episode_number": episode_num,
        }
        await add_credit(credit)

    episode = {
        "number": episode_num,
        "title": episode_title,
        "date": episode_date,
        "length": episode_length,
        "artist": episode_artist,
    }

    await add_episode(episode)

    art_credit = {
        "producer": episode_artist,
        "type": "Artist",
        "episode_number": episode_num,
    }

    await add_credit(art_credit)

    print(f"======== Finished processing episode {episode_num} ========")

async def update_database():
    latest_saved = await last_episode_saved()
    newest_ep = await newest_episode()
    if latest_saved == newest_ep:
        print("The database is up to date")
        return 0
    for i in range(latest_saved + 1, newest_ep + 1):
        await process_episode(i)

async def process_batch(first, last):
    for i in range(first, last + 1):
        await process_episode(i)

asyncio.run(update_database())
# asyncio.run(process_episode(612))
# asyncio.run(process_batch(616, 1520))

if __name__ == "__main__":
    asyncio.run(update_database())
