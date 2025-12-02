from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.db.models.billing import Payment
from app.schemas.payments import PaymentCreate, PaymentResponse
from app.services.payments.payment_service import PaymentService  # 👈 added import

router = APIRouter(tags=["payments"])

@router.post("/", response_model=PaymentResponse, status_code=201)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    """Create a new payment."""
    try:
        service = PaymentService(db)
        return service.create_payment(payment.amount)
    except Exception as e:
        print("❌ Payment creation failed:", e)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[PaymentResponse])
def list_payments(db: Session = Depends(get_db)):
    """List all payments ordered by creation date."""
    try:
        service = PaymentService(db)
        return service.get_all_payments()
    except Exception as e:
        print("❌ Payment list failed:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
