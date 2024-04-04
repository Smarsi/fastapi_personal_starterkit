from errors import APIError

async def ExampleValidator(log_file):

    # Here you can put your validation logic
    # If some error ocours, you can raise an APIError
    # if True:
    #     raise APIError(
    #         status_code=200,
    #         detail="Some error ocurred"
    #     )

    return True
