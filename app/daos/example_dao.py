from app.database.connection import get_database
from sqlalchemy import text # text is used to prevent SQL Injection

#from errors import APIError # if needed

# Logs Import
from logger_config import log_writer

# Models Import
from app.api.models.example_model import ExampleModel

class prefix_entity_DAO:
    async def get_sequence(self):
        db = get_database()
        query = text(f"SELECT nextval('prefix_entity_seq')")
        result = await db.execute(query)
        return result
