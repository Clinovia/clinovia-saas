"""
Handles invoice generation and retrieval.
"""

import stripe
from app.core.config import settings


class InvoiceService:
    def __init__(self):
        stripe.api_key = settings.STRIPE_API_KEY

    def create_invoice(self, customer_id: str) -> dict:
        """Create a new invoice for a customer."""
        try:
            invoice = stripe.Invoice.create(customer=customer_id, auto_advance=True)
            return invoice
        except Exception as e:
            raise RuntimeError(f"Stripe invoice error: {e}")

    def list_invoices(self, customer_id: str, limit: int = 10) -> dict:
        """List past invoices."""
        try:
            return stripe.Invoice.list(customer=customer_id, limit=limit)
        except Exception as e:
            raise RuntimeError(f"Stripe list invoices failed: {e}")
