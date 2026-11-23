from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.schemas.organizations_schema import org_create,org_response
from app.services.organizations_servics import find_org,create_org
from app.core.database import get_db
org_router = APIRouter(
    prefix="/organizations",
    tags = ["organizations - api"]
)

@org_router.post('/',response_model=org_response)
def new_organization(curr_org : org_create,db : Session =  Depends(get_db)) :
    return create_org(curr_org,db)

@org_router.get('/{org_id}')
def find_organization(org_id : int,db : Session = Depends(get_db)) :
    return find_org(org_id,db)