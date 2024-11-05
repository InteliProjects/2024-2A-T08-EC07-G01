from contextlib import asynccontextmanager
from dotenv import dotenv_values
import motor.motor_asyncio

config = dotenv_values(".env")


client = motor.motor_asyncio.AsyncIOMotorClient(config["DATABASE_URI"])
db = client.get_database("cross_the_line")
knr_collection = db.get_collection("knr")

print("Populating KNR collection")

client.close()
