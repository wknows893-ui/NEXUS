from pydantic import BaseModel,EmailStr,ConfigDict
from datetime import datetime

class org_create(BaseModel) :

    name : str
    slug : str
    description : str
    owner_id : int


class org_response(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    name : str
    id : int
    owner_id : int
    description : str
    created_at : datetime