# backend/app/api/routes/billing.py
from app.services.billing import invoice_service, subscription_service, utils
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(tags=["Billing"])


# Dependency injection
async def get_subscription_service():
    return subscription_service.SubscriptionService()


async def get_invoice_service():
    return invoice_service.InvoiceService()


# ===============================
# Subscription Endpoints
# ===============================
@router.post("/subscriptions/create")
async def create_subscription(
    customer_id: str,
    price_id: str,
    service: subscription_service.SubscriptionService = Depends(get_subscription_service),
):
    """
    Create a Stripe subscription for a given customer.
    """
    try:
        subscription = service.create_subscription(customer_id, price_id)
        return {"status": "success", "subscription": subscription}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/subscriptions/{subscription_id}")
async def cancel_subscription(
    subscription_id: str,
    service: subscription_service.SubscriptionService = Depends(get_subscription_service),
):
    """
    Cancel an active Stripe subscription.
    """
    try:
        result = service.cancel_subscription(subscription_id)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ===============================
# Invoice Endpoints
# ===============================
@router.post("/invoices/create")
async def create_invoice(
    customer_id: str, service: invoice_service.InvoiceService = Depends(get_invoice_service)
):
    """
    Create an invoice for a Stripe customer.
    """
    try:
        invoice = service.create_invoice(customer_id)
        return {"status": "success", "invoice": invoice}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/invoices/list/{customer_id}")
async def list_invoices(
    customer_id: str, service: invoice_service.InvoiceService = Depends(get_invoice_service)
):
    """
    Retrieve a list of invoices for a Stripe customer.
    """
    try:
        invoices = service.list_invoices(customer_id)
        return {"status": "success", "invoices": invoices}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ===============================
# Utility Endpoint
# ===============================
@router.get("/tax")
async def calculate_tax_endpoint(amount: float):
    """
    Calculate estimated tax for a given amount.
    """
    tax = utils.calculate_tax(amount)
    return {"amount": amount, "estimated_tax": tax}

print(f"Module path: {__file__}")

