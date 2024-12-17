from pydantic import BaseModel, Field

class UserRequest(BaseModel):
   username: str = Field(..., min_length=3, max_length=30)
   password: str = Field(..., min_length=6, max_length=50)

class UserLogin(BaseModel):
    username: str
    password: str
