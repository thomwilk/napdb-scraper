from bs4 import BeautifulSoup
import aiohttp
import aiofiles
import os
from PIL import Image


async def extractor(epNum):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.noagendashow.net/listen/{epNum}") as response:
            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")
    episode_date = soup.select_one("#swup > section:nth-child(5) > div.section-buttons-full > a:nth-child(1)")[
        "href"].split("NA-")[1].split("-Final")[0]
    episode_title = soup.title.text.split("No Agenda ")[1].split(": ")[1]
    episode_length = soup.select_one(".hero-text > div").text.split(" • ")[1]
    episode_artist = soup.select_one(
        "#swup > section:nth-child(4) > div > p:nth-child(9)").text
    executive_producers = soup.select_one(
        "#swup > section:nth-child(4) > div > p:nth-child(5)").text.split(", ")
    associate_producers = soup.select_one(
        "#swup > section:nth-child(4) > div > p:nth-child(7)").text.split(", ")

    epInfo = {
        "epDate": episode_date,
        "epTitle": episode_title,
        "epLength": episode_length,
        "epArtist": episode_artist,
        "epExecs": executive_producers,
        "epAssocs": associate_producers,
    }

    return epInfo


async def newest_episode():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.noagendashow.net") as response:
            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")
    episode_num = soup.select_one(
        "#swup > section:nth-child(2) > div.episodes > a:nth-child(2) > h3").text.split(":")[0]

    return int(episode_num)
