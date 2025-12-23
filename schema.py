from pydantic import BaseModel, ConfigDict
from typing import Optional


# SCHEMAS (Pydantic models)
class UserCreate(BaseModel):
    username: str
    email: str
    branch: str
    team: str
    password: str
    role: str = "user"


class UserLogin(BaseModel):
    username: str
    password: str

# JWT schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    branch: str
    team: str
    role: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
