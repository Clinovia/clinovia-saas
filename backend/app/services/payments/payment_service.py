from sqlalchemy.orm import Session
from app.db.models.billing import Payment


class PaymentService:
    """Service layer for handling payment operations."""

    def __init__(self, db: Session):
        self.db = db

    def create_payment(self, amount: float, status: str = "completed"):
        """Create a new payment record."""
        payment = Payment(amount=amount, status=status)
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def get_all_payments(self):
        """Retrieve all payments ordered by creation date."""
        return self.db.query(Payment).order_by(Payment.created_at.desc()).all()

    def get_payment_by_id(self, payment_id: int):
        """Retrieve a specific payment by its ID."""
        return self.db.query(Payment).filter_by(id=payment_id).first()
