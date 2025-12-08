from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class Subscription(BaseModel):
    __tablename__ = "subscriptions"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan = Column(String, nullable=False)
    status = Column(String, nullable=False)
    started_at = Column(String, nullable=False)  # Or DateTime if you want timestamps
    ended_at = Column(String, nullable=True)    # Or DateTime

    # Relationship to User
    user = relationship("User", back_populates="subscriptions")
    

class Payment(BaseModel):
    __tablename__ = "payments"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    status = Column(String, nullable=False)
    payment_method = Column(String, nullable=True)

    # Relationships
    user = relationship("User", back_populates="payments")
