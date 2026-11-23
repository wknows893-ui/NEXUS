from app.schemas.users_schema import UserCreate,UserResponse,UserUpdate
from sqlalchemy.orm import Session
from app.core.security import hash_password,verify_password
from app.models.users_model import User
from app.repos.users_repo import finduser_byemail,save,finduser_byid,save_n_ref_user
from fastapi import HTTPException,status

def existing_user_check(uss : UserCreate,db : Session) : 
    user_exists = finduser_byemail(db,uss.email)
    if user_exists :
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
                            detail = "User with such email already exists !" )
    
def create_new_user(uss : UserCreate,db : Session) :
        existing_user_check(uss,db)

        hashed_password = hash_password(uss.password)
        new_user = User(
            name =  uss.name,
            email = uss.email,
            password_hash = hashed_password,
            status = 'ACTIVE',
        )
        new_user = save(db,new_user)

        return UserResponse.model_validate(new_user)

def findx_user(user_id : int,db : Session):
     user_exists = finduser_byid(db,user_id)
     if user_exists is None :
          raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                              detail = "no user exists with such id")
     return UserResponse.model_validate(user_exists)

def deact_user(user_id : int,db : Session) :
     user_exists = finduser_byid(db,user_id)
     if user_exists is None :
               raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                                   detail = "no user exists with such id")
     user_exists.status = "INACTIVE"
     db.commit()
     return 

def update_service(user_id : int,changes : UserUpdate , db : Session):
     user = finduser_byid(db,user_id)
     if user is None : 
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                               detail = "No user exists with such id")
     chn_nig = changes.model_dump(exclude_unset=True)

     for field,value in chn_nig.items() : 
           setattr(user,field,value)
     user = save_n_ref_user(db,user)
     return UserResponse.model_validate(user)