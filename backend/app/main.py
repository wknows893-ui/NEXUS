from fastapi import FastAPI
from app.api.users_api import router

app = FastAPI()
app.include_router(router)

@app.get('/health')
def health_check() :
    return {"status" : "ok"}

