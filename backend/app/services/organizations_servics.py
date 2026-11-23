from app.schemas.organizations_schema import org_create,org_response
from app.models.organizations_model import Organization
from app.repos.organizations_repo import find_org_by_name,find_org_by_id,save
from sqlalchemy.orm import Session
from fastapi import HTTPException,status


def find_org(curr_org : int,db : Session) :
    res = find_org_by_id(db,curr_org)
    return org_response.model_validate(res)

def create_org(curr_org : org_create,db : Session) :
    res = find_org_by_name(db,curr_org.name)
    if res :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail = "Organization with such name already exists!! ")
    new_org = Organization(
         name = curr_org.name,
         slug = curr_org.slug,
         description = curr_org.description,
         owner_id = curr_org.owner_id,
    )
    new_org = save(db,new_org)
    return org_response.model_validate(new_org)