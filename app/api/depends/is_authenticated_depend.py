from fastapi import Depends, Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Logs Import
from logger_config import Logger

# DAOS Import
# from app.daos.route_dao import nt_route_DAO
# route_dao = nt_route_DAO()
from app.daos.user_dao import UserDAO

# Utils Import
from app.utils.token_manager import decode as token_decoder

security = HTTPBearer()

async def verify_authentication(request: Request, credentials: HTTPAuthorizationCredentials=Depends(security)):
    user_dao = UserDAO()
    logger: Logger = request.state.logger
    token = credentials.credentials

    if token:
        decoded_token = await token_decoder(token)  # Passing token
        logger.write(f"VERIFY AUTHENTICATION - Result of decoded token {decoded_token}")
        user = await user_dao.get_user_by_token(token, logger)
        if user and 'id_user' in decoded_token:
            request.state.requester = {"authenticated": True, "decoded_token": decoded_token}
            return {
                "authenticated": True,
                "decoded_token": decoded_token               
            }
        raise HTTPException(status_code=401, detail="Unauthorized - Invalid Token")
    raise HTTPException(status_code=401, detail="Unauthorized - Token not provided")

# CAUTION: Used in case you want to control the permissions via database (using tables and registries)
# async def verify_authorization(request: Request):
#     log_file = request.state.log_file
#     requester = request.state.requester
#     destination = request.__dict__['scope']['route'].path
#     destination = destination[:-1] if destination[-1] == "/" else destination
#     method = request.__dict__['scope']['method'].lower()
#     log_writer(log_file, f"Depend - Request to endpoint: {destination}. Method: {method}")
#     destination_needed_permissions = await route_dao.select_route_permissions(destination, method, log_file)
#     if destination_needed_permissions:
#         for permission in destination_needed_permissions:
#             permission = dict(permission)
#             if permission['title'] not in requester['decoded_token']['permissions']:
#                 raise HTTPException(status_code=403, detail="Unauthorized - Permission Denied!")
#     return True    
    