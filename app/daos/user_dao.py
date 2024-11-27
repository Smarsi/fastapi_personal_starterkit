from sqlalchemy.sql import text

# Database Import
from app.database.connection import get_database

# Models Import
from app.api.models. user_model import UserModelOnCreation

# Logs Import
from logger_config import Logger

class UserDAO():

    def __init__(self):
        self.db = get_database()

    async def _get_sequence(self):
        db = self.db
        query = text("SELECT nextval('sys_user_seq')")
        result = await db.execute(query)
        return result

    async def create_user(self, data: UserModelOnCreation, logger: Logger) -> int | bool:
        logger.write(f"DAO - On UserDAO create_user. Received Data: {data}")
        db = self.db
        id_user = await self._get_sequence()
        query = text(f"""
                    INSERT INTO sys_user(
                        id_user, 
                        username, 
                        email, 
                        password, 
                        created_at_ts,
                        created_by,
                        change_password
                    ) VALUES (
                        {id_user},
                        '{data['username']}',
                        '{data['email']}',
                        '{data['password']}',
                        '{data['created_at_ts']}',
                        {data['created_by']},
                        '{data['change_password']}'                      
                    );
                     
        """)
        logger.write(f"DAO - Query to be executed on database: {query}")
        result = await db.execute(query)
        logger.write(f"DAO - Result from database: {result}")
        if not result:
            return id_user
        logger.write(f"DAO - Database returned something... Possible error: {result}")
        return False

    async def get_user_by_id(self):
        pass

    async def get_user_by_email(self, email: str, logger: Logger):
        logger.write(f"DAO - On UserDAO get_user_by_email. Received emal: {email}")
        db = self.db
        query = text(f"SELECT * FROM sys_user WHERE email = '{email}'")
        logger.write(f"DAO - Query to be executed on database: {query}")
        result = await db.fetch_one(query)
        logger.write(f"DAO - Result from database: {result}")
        return result
    
    async def get_user_by_token(self, token: str, logger: Logger):
        logger.write(f"DAO - On UserDAO get_user_by_token. Received token: {token}")
        db = self.db
        query = text(f"SELECT * FROM sys_user WHERE token = '{token}'")
        logger.write(f"DAO - Query to be executed on database: {query}")
        result = await db.fetch_one(query)
        logger.write(f"DAO - Result from database: {result}")
        return result
    
    async def update_user_login(self, data: dict, logger: Logger):
        logger.write(f"DAO - On UserDAO update_user_login. Received Data: {data}")
        db = self.db
        query = text(f"""
                    UPDATE sys_user
                    SET last_login = '{data['last_login']}',
                        token = '{data['token']}'
                    WHERE id_user = {data['id_user']};
        """)
        logger.write(f"DAO - Query to be executed on database: {query}")
        result = await db.execute(query)
        logger.write(f"DAO - Result from database: {result}")
        if not result:
            return True
        logger.write(f"DAO - Database returned something... Possible error: {result}")
        return result
    