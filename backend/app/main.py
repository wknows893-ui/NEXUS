from fastapi import FastAPI
from app.api.users_api import user_router
from app.api.organizations_api import org_router

app = FastAPI()
app.include_router(user_router)
app.include_router(org_router)
@app.get('/health')
def health_check() :
    return {"status" : "ok"}

