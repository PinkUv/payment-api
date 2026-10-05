from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.transaction import Transaction

router = APIRouter(prefix='/transactions', tags=['transactions'])

@router.get("/{transaction_id}")
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    # 1. query transaction by transaction_id
    #    if not found, raise 404
    current_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not current_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # 2. return transaction details
    return {
        "transaction_id": current_transaction.id,
        "from_account_id": current_transaction.from_account_id,
        "to_account_id": current_transaction.to_account_id,
        "amount": current_transaction.amount,
        "status": current_transaction.status,
        "created_at": current_transaction.created_at
    }