from pymongo import MongoClient
from os import getenv

client = MongoClient(getenv("MONGODB_URI"))

async def add_credit(credit):
    if credit["producer"].strip() == "":
        return

    db = client["NAPDB"]
    collection = db["credits"]

    exists = collection.find_one({
        "producer": credit["producer"],
        "type": credit["type"],
        "episode_number": credit["episode_number"],
    })

    if exists is not None:
        return "Credit already saved"

    if credit["type"] == "Artist" and "getalby.com" in credit["producer"]:
        arr = credit["producer"].split(" ")
        credit["cryptoAddress"] = arr[-1]
        arr.pop()
        credit["producer"] = " ".join(arr).rstrip(" -")

    collection.insert_one(credit)
    print(f'{credit["type"]} producer credit saved for {credit["producer"]}, Episode: {credit["episode_number"]}')

async def add_episode(episode):
    db = client["NAPDB"]
    collection = db["episodes"]

    exists = collection.find_one({"number": episode["number"]})

    if exists is not None:
        return f'Episode number {episode["number"]} already saved'
    
    collection.insert_one(episode)
    print(f'Episode {episode["number"]}: {episode["title"]} saved')

async def last_episode_saved():
    db = client["NAPDB"]
    collection = db["episodes"]

    last_episode_saved = list(collection.find().sort("number", 1))
    return last_episode_saved[-1]["number"]
