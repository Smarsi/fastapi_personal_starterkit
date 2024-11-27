from pydantic import BaseModel, StrictStr, StrictInt, StrictBool, StrictFloat

class UserModelOnCreation(BaseModel):
    username: StrictStr
    email: StrictStr
    password: StrictStr
    created_at_ts: StrictStr
    created_by: StrictInt
    change_password: StrictBool

    @staticmethod
    def json_model(self):
        return {
            "username": self.model_fields["username"].name,
            "email": self.model_fields["email"].name,
            "password": self.model_fields["password"].name,
            "created_at_ts": self.model_fields["created_at_ts"].name,
            "created_by": self.model_fields["created_by"].name,
            "change_password": self.model_fields["change_password"].name
        }