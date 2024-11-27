import datetime
from fastapi import HTTPException
from passlib.context import CryptContext

# Schemas Import
from app.api.schemas.authorization_schemas import LoginFieldsSchema, RegisterFieldsSchema

# Model Import
from app.api.models.global_responses_models import Global_Created_Response_Model
from app.api.models.user_model import UserModelOnCreation

# DAOs Import
from app.daos.user_dao import UserDAO

# Errors Import
from errors import APIError

# Utils Import
from app.utils.token_manager import encode, decode, validate
from app.utils.datetime_manager import get_current_datetime

# Logs Import 
from logger_config import Logger


async def login_controller(received_data: LoginFieldsSchema, logger: Logger) -> str:
    logger.write(f"Controller - On AuthController Login. Received data: {received_data.email}")

    dao = UserDAO()
    result = await dao.get_user_by_email(received_data.email, logger)

    if not result:
        raise HTTPException(status_code=401, detail="Error - Account not found")
    
    # === Check Password ====
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(received_data.password, result['password']):
        raise HTTPException(status_code=401, detail="Error - Invalid Password")

    # === Generate Token ====
    token_payload = {"email": received_data.email, "id_user": result['id_user'], "username": result['username']}
    token = await encode(token_payload)

    # === Register Token & Last Login ===
    data = {
        "id_user": result['id_user'],
        "token": token,
        "last_login": datetime.datetime.now()
    }
    update = await dao.update_user_login(data, logger)
    if update:
        response = {
            "token": token,
            "id_user": result['id_user'],
            "username": result['username']
        }
        return response
    raise APIError("Controller", "Error - Cannot check user login... Try again later!")


async def register_controller(requester: dict, received_data: RegisterFieldsSchema, logger: Logger) -> Global_Created_Response_Model:
    logger.write(f"Controller - On AuthController Register. Received data: {{username: {received_data.username}, email: {received_data.email}}}")

    dao = UserDAO()
    
    # === Check if email is already in use ===
    result = await dao.get_user_by_email(received_data.email, logger)
    if result:
       raise APIError("Controller", "Error - Email already in use") 
    # ==== Check if email is already in use ===

    crpcontext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    data = UserModelOnCreation(**received_data.model_dump(), created_by=requester['id_user'], change_password=False, created_at_ts=get_current_datetime())

    success = await dao.create_user(data, logger)
    if not success:
        raise APIError("Controller", "Error - Could not create user")
    
    return Global_Created_Response_Model(
        item_id=success,
        message="User created successfully",
    )