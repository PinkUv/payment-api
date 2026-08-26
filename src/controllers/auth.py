from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.database import get_db
from src.models.user import User
from src.models.account import Account
import bcrypt, jwt, os


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

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == body.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not bcrypt.checkpw(body.password.encode(), user.password_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"user_id": user.id}, os.getenv("JWT_SECRET"), algorithm="HS256")

    return {"token": token}