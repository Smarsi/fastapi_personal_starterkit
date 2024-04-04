# Errors Import
from errors import APIError

# Logs Import
from logger_config import log_writer

# Models Import
from app.api.models.example_model import ExampleModel

# Validators Import
from app.api.validators.example_validator import ExampleValidator

async def First_Endpoint_Controller(requester, log_file):

    ## Here you can put your business logic

    ## If some error ocours, you can raise an APIError
    # if True:
    #     raise APIError(
    #         status_code=200,
    #         detail="Some error ocurred"
    #     )

    # For Good Practice allways return a model
    # If your controller don't have one model to return, you can use a Global Response Model (created, updated, deleted)

    # If you need to access database or other services, you can import them and use here (external requests, third-part-applications, etc);
    # data = await example_dao.get_data_from_database(log_file)

    data_on_model = ExampleModel(
        name="Test",
        description="This is a test",
        value=1,
        is_active=True,
        is_deleted=False
    )

    return data_on_model
