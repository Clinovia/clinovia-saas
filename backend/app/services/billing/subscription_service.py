"""
Handles Stripe subscription management.
"""

import stripe
from app.core.config import settings


class SubscriptionService:
    def __init__(self):
        stripe.api_key = settings.STRIPE_API_KEY

    def create_subscription(self, customer_id: str, price_id: str) -> dict:
        """Create a Stripe subscription for a given customer."""
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{"price": price_id}],
            )
            return subscription
        except Exception as e:
            raise RuntimeError(f"Stripe subscription error: {e}")

    def cancel_subscription(self, subscription_id: str) -> dict:
        """Cancel an existing Stripe subscription."""
        try:
            return stripe.Subscription.delete(subscription_id)
        except Exception as e:
            raise RuntimeError(f"Failed to cancel subscription: {e}")
