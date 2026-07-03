from fastapi import FastAPI, APIRouter
from src.controllers.auth import router
import src.models.user
import src.models.account
from src.database import Base, engine


app = FastAPI(title="Payment API")
Base.metadata.create_all(bind=engine)
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}