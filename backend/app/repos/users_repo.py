from sqlalchemy.orm import Session
from app.models.users_model import User

def finduser_byemail(db : Session,email : str) :
    return db.query(User).filter(User.email == email).first()

def finduser_byid(db : Session,user_id : int) :
    return db.query(User).filter(User.id == user_id).first()

def save(db : Session,user : User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def save_n_ref_user(db : Session,usernig : User) -> User:
    db.commit()
    db.refresh(usernig)
    return usernig
