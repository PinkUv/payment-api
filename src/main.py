from fastapi import FastAPI, APIRouter
from src.controllers.auth import router
from src.controllers.transfers import router as transferRouter
from src.controllers.transactions import router as transactionRouter
from src.controllers.accounts import router as accountRouter
import src.models.user
import src.models.account
from src.database import Base, engine


app = FastAPI(title="Payment API")
Base.metadata.create_all(bind=engine)

app.include_router(router)
app.include_router(transferRouter)
app.include_router(transactionRouter)
app.include_router(accountRouter)

@app.get("/health")
def health():
    return {"status": "ok"}