import os
import databases
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DATABASE_POOL_MIN_SIZE = int(os.getenv("DATABASE_POOL_MIN_SIZE"))
DATABASE_POOL_MAX_SIZE = int(os.getenv("DATABASE_POOL_MAX_SIZE"))

# Build the database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" # Example: postgresql://user:password@localhost:5432/database

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