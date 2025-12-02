# backend/app/jobs/trial_reminder.py
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.models.users import User
from app.db.base import SessionLocal
from app.services.stripe_service import create_checkout_session
from app.core.config import settings
from some_email_library import send_email  # Replace with your email service

def send_trial_expiration_reminders():
    db: Session = SessionLocal()
    try:
        # Users whose trial ends in 2 days
        soon_to_expire = db.query(User).filter(
            User.subscription_status == "trial",
            User.enterprise_interest == False,  # only self-serve
            User.trial_end_date <= datetime.utcnow() + timedelta(days=2),
            User.trial_end_date >= datetime.utcnow()
        ).all()

        for user in soon_to_expire:
            if not user.stripe_customer_id:
                continue  # Cannot generate checkout without Stripe customer

            # Create Stripe checkout session
            price_id = settings.STRIPE_PROFESSIONAL_PRICE_ID  # Set in config
            success_url = f"{settings.FRONTEND_URL}/dashboard"
            cancel_url = f"{settings.FRONTEND_URL}/trial"

            checkout_url = create_checkout_session(
                customer_id=user.stripe_customer_id,
                price_id=price_id,
                success_url=success_url,
                cancel_url=cancel_url
            )

            # Send reminder email
            send_email(
                to=user.email,
                subject="Your 30-Day Trial is Ending Soon",
                body=f"""
Hi {user.name},

Your 30-day trial is ending soon. Click below to continue your subscription:

{checkout_url}

Thank you,
The Team
                """
            )
    finally:
        db.close()


# Optional: For direct script testing
if __name__ == "__main__":
    send_trial_expiration_reminders()
