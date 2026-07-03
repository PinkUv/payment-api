from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.database import get_db
from src.models.user import User
from src.models.account import Account
import bcrypt

router = APIRouter(prefix='/auth', tags=['auth'])

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

@router.post("/register", status_code=201)
def register(body: RegisterRequest, db: Session = Depends(get_db)):

    # Check if user already exists
    if db.query(User).filter(or_(User.email == body.email, User.username == body.username)).first():
        raise HTTPException(status_code=400, detail="Username or email already taken")
    
    password_hash = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt()).decode()
    
    user = User(username = body.username, email = body.email, password_hash = password_hash)

    db.add(user)
    db.flush()
    account = Account(user_id=user.id)
    db.add(account)
    db.commit()
    db.refresh(user)

    return {"message": "User created", "user_id": user.id}
