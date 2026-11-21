from fastapi import FastAPI,Depends
from fastapi import APIRouter,HTTPException
from app.schemas.user_schema import UserCreate,UserResponse,UserUpdate
from app.services.user_service import create_new_user,findx_user,deact_user,update_service
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter(
    prefix = "/users",
    tags=['users']
)
app = FastAPI()

@router.get('/')
def home() :
    return {"health" : "✅",
            "version" : "0.000"}

# CREATE A NEW USER
@router.post('/',response_model= UserResponse)
def new_user(curr_user : UserCreate,db : Session = Depends(get_db)):
    return create_new_user(curr_user,db)

# FIND A USER
@router.get('/{user_id}',response_model= UserResponse)
def find_user(user_id : int,db : Session = Depends(get_db)):
    return findx_user(user_id,db)

# UPDATE A USER
@router.patch('/{user_id}',response_model= UserResponse)
def update_user(user_id : int,user_upd : UserUpdate,db : Session = Depends(get_db)) :
    return update_service(user_id,user_upd,db)

# DEACTIVATE A USER
@router.delete('/{user_id}')
def deactivate_user(user_id : int,db : Session = Depends(get_db)) : 
    deact_user(user_id,db)
    return {'message' : 'Deactivated Successfully !!'}
