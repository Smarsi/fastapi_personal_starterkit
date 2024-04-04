import os
import databases
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("URL")
DATABASE_POOL_MIN_SIZE = int(os.getenv("DATABASE_POOL_MIN_SIZE"))
DATABASE_POOL_MAX_SIZE = int(os.getenv("DATABASE_POOL_MAX_SIZE"))
database = databases.Database(DATABASE_URL, min_size=DATABASE_POOL_MIN_SIZE, max_size=DATABASE_POOL_MAX_SIZE)

Base = declarative_base()

async def connect_to_database(new_database):
    global database
    await new_database.connect()
    database = new_database
    
async def close_database_connection():
    await database.disconnect()

def get_database():
    return database