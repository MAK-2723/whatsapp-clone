from motor.motor_asyncio import AsyncIOMotorClient
from os import getenv
from dotenv import load_dotenv
import logging

load_dotenv()
logger=logging.getLogger("database")

MONGO_URI=getenv("MONGO_URI")
if not MONGO_URI:
  logger.error("MONGO_URI not set in env")
  raise RuntimeError("MONGO_URI not set")
  
client=AsyncIOMotorClient(MONGO_URI)
db=client.whatsapp

messages=db.processed_messages
