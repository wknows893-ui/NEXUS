from sqlalchemy.orm import Session
from app.models import Organization

def save(db : Session,org : Organization) :
    db.add(org)
    db.commit()
    db.refresh(org)
    return org

def find_org_by_name(db : Session,org_name : str) : 
    return  db.query(Organization).filter(Organization.name == org_name).first()

def find_org_by_id(db : Session,org_id: int) : 
    return  db.query(Organization).filter(Organization.id == org_id).first()