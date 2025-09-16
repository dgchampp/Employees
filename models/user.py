from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
