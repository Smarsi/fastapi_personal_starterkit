from pydantic import BaseModel, StrictBool, field_validator, StrictStr
from typing import Any
from typing import Optional
from datetime import time


class LoginFieldsSchema(BaseModel):
    email: StrictStr
    password: StrictStr

    @field_validator("email")
    def email_must_be_valid(cls, value):
        if "@" not in value or "." not in value or value == "":
            raise ValueError("Invalid email address")
        return value

    @classmethod
    def json_model(cls):
        return {
            "email": cls.model_fields["email"].name,
            "password": cls.model_fields["password"].name
        }

class RegisterFieldsSchema(BaseModel):
    username: StrictStr
    email: StrictStr
    password: StrictStr
    password_confirmation: StrictStr

    @field_validator("email")
    def email_must_be_valid(cls, value):
        if "@" not in value or "." not in value or "" == value:
            raise ValueError("Invalid email address")
        return value
    
    @field_validator("password")
    def password_must_be_valid(cls, value):
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters")
        return value
        
    @field_validator("password_confirmation")
    def password_confirmation_must_be_valid(cls, value, values):
        if "password" in values.data.keys() and values.data["password"] != value:
            raise ValueError("Passwords do not match")
        return value
        
    @staticmethod
    def json_model(self):
        return {
            "username": self.model_fields["username"].name,
            "email": self.model_fields["email"].name,
            "password": self.model_fields["password"].name,
            "password_confirmation": self.model_fields["password_confirmation"].name
        }
