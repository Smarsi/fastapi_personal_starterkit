from fastapi import APIRouter, Depends, Request, Body

# Logs Import
from logger_config import Logger

# Schema Import
from app.api.schemas.response_schema import GlobalResponse, GlobaResponsesExamples, build_reponse_example
from app.api.schemas.authorization_schemas import LoginFieldsSchema, RegisterFieldsSchema

# Depends Import
from app.api.depends.is_authenticated_depend import verify_authentication

# Controllers Import
from app.api.controllers.auth_controllers import login_controller, register_controller

# Models Import
from app.api.models.example_model import ExampleModel

router = APIRouter(
    prefix='/auth',
    tags=["Authorization Routes"]
)

def get_tag_description():
    return {
        "name": "Authorization Routes",
        "description": """ Rotes used to authenticate and authorize users. """
    }


@router.post("/login", response_model=GlobalResponse, response_model_exclude_unset=False, responses={**GlobaResponsesExamples})
async def login_router(request: Request, body: LoginFieldsSchema = Body(...)):
    logger: Logger = request.state.logger
    logger.write(f"Login Route - Requested. Received: {body.email}")

    controller = await login_controller(body, logger)

    response = GlobalResponse(
        status=True,
        request_id=request.state.uuid,
        data=controller
    )
    response.set_start_ts(request.state.start_ts)
    return response


@router.post("/register", response_model=GlobalResponse, include_in_schema=False)
async def register_router(request: Request, body: RegisterFieldsSchema = Body(...), depends: dict = Depends(verify_authentication)):
    logger: Logger = request.state.logger
    logger.write(f"Register Route - Requested. Received: {body.email}")

    controller = await register_controller({"id_user": 0}, body, logger)

    response = GlobalResponse(
        status=True,
        request_id=request.state.uuid,
        data=controller
    )
    response.set_start_ts(request.state.start_ts)
    return response
