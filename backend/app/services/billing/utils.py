"""
Billing Utility Functions
"""


def format_currency(amount: float, currency: str = "usd") -> str:
    """Format numeric amount as currency string."""
    return f"{amount/100:.2f} {currency.upper()}"


def calculate_tax(amount: float, rate: float = 0.1) -> float:
    """Calculate tax on given amount (default 10%)."""
    return amount * rate
