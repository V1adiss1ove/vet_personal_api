from fastapi import FastAPI

from app.api.main import api_router

app = FastAPI(title="Vet Personal", version="0.1.0")
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "ok"}
