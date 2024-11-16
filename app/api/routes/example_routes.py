from fastapi import APIRouter, Depends, Request, Body

# Logs Import
from logger_config import Logger, log_writer

# Schema Import
from app.api.schemas.response_schema import GlobalResponse, GlobaResponsesExamples, build_reponse_example

# Depends Import
from app.api.depends.is_authenticated_depend import verify_authentication #, verify_authorization

# Controllers Import
from app.api.controllers.example_controller import First_Endpoint_Controller

# Models Import
from app.api.models.example_model import ExampleModel

router = APIRouter(
    prefix='/example',
    tags=["First Example Routes"]
)

def get_tag_description():
    return {
        "name": "First Example Routes",
        "description": """ Example route to show how to work with this starterpack. """
    }

@router.get("/", response_model=GlobalResponse, response_model_exclude_unset=False, responses={**GlobaResponsesExamples, **build_reponse_example(200, ExampleModel, "Success - Example response doc for a GET 200O-OK")})
# def First_Route(request: Request, requester: dict = Depends(verify_authentication), authorized: bool = Depends(verify_authorization)):
async def First_Endpoint(request: Request, requester: dict = Depends(verify_authentication)):
    logger: Logger = request.state.logger
    logger.write("First Route - Requested")
    
    controller = await First_Endpoint_Controller(requester, logger)

    response = GlobalResponse(
        status=True,
        request_id=request.state.request_id,
        data=controller,
    )
    response.set_start_ts(request.state.start_ts)
    return response


