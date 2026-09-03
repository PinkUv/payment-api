from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from src.database import get_db
from src.models.account import Account
from src.models.transaction import Transaction
from decimal import Decimal

router = APIRouter(prefix='/transfers', tags=['transfers'])

class TransferRequest(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: Decimal
    idempotency_key: str

@router.post("/", status_code=201)
def transfer(body: TransferRequest, db: Session = Depends(get_db)):

    existing = db.query(Transaction).filter(Transaction.idempotency_key == body.idempotency_key).first()
    if existing:
        return {"transaction_id": existing.id, "status": existing.status}

    from_account = db.query(Account).filter(Account.id == body.from_account_id).first()
    if not from_account:
        raise HTTPException(status_code=404, detail="Account not found")

    if from_account.balance < body.amount:
        raise HTTPException(status_code=400, detail="Insufficent Funds")

    to_account = db.query(Account).filter(Account.id == body.to_account_id).first()
    if not to_account:
        raise HTTPException(status_code=404, detail="Account not Found")
    
    try:
        from_account.balance -= body.amount
        to_account.balance += body.amount
        transaction = Transaction(
        from_account_id=body.from_account_id,
        to_account_id=body.to_account_id,
        amount=body.amount,
        idempotency_key=body.idempotency_key
        )
        db.add(transaction)
        db.commit()
        return {"transaction_id": transaction.id, "status": transaction.status}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Transfer Failed")
    