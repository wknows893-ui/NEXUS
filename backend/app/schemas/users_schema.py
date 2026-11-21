from pydantic import BaseModel,EmailStr,ConfigDict

class UserCreate(BaseModel) :
    name : str
    email : EmailStr
    password : str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    name : str
    email : EmailStr
    status : str | None
    avatar_url : str | None

class UserUpdate(BaseModel) :
    name : str | None = None
    avatar_url : str | None = None