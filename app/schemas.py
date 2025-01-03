from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

class UserRequest(BaseModel):
   username: str = Field(..., min_length=3, max_length=30)
   password: str = Field(..., min_length=6, max_length=50)
   name: str = Field(..., min_length=2, max_length=50)
   lastname: str = Field(..., min_length=2, max_length=100)
   email: EmailStr  # Validación email, utilizamos EmailStr para validar correos
   phone_number: PhoneNumber  # Validación de teléfono obligatorio
   

class UserLogin(BaseModel):
    username: str
    password: str
