from fastapi import FastAPI, APIRouter
from src.controllers.auth import router
from src.controllers.transfers import router as transferRouter
import src.models.user
import src.models.account
from src.database import Base, engine


app = FastAPI(title="Payment API")
Base.metadata.create_all(bind=engine)
app.include_router(router)

app.include_router(transferRouter)

@app.get("/health")
def health():
    return {"status": "ok"}