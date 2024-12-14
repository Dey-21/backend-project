from pydantic import BaseModel

class UserRequest(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str
