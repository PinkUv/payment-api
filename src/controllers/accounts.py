from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.account import Account

router = APIRouter(prefix='/accounts', tags=['accounts'])

@router.get("/{account_id}/balance")
def get_balance(account_id: int, db: Session = Depends(get_db)):
    # 1. query account by account_id
    #    if not found, raise 404
    current_account = db.query(Account).filter(Account.id == account_id).first()
    if not current_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # 2. return account balance
    return {"message": "Account Balance", "acc_balance": current_account.balance}