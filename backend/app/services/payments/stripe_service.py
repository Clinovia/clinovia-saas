# backend/app/services/stripe_service.py
import stripe
from app.core.config import settings

stripe.api_key = settings.STRIPE_API_KEY  # Add this in your config.py

def create_stripe_customer(email: str, name: str) -> str:
    """Create a Stripe customer and return customer ID."""
    customer = stripe.Customer.create(
        email=email,
        name=name
    )
    return customer.id

def create_checkout_session(customer_id: str, price_id: str, success_url: str, cancel_url: str) -> str:
    """Create a Stripe checkout session and return the session URL."""
    session = stripe.checkout.Session.create(
        customer=customer_id,
        payment_method_types=["card"],
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session.url
