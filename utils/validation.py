from datetime import date

#It validates the text
def validate_required_text(value, field_name="value"):
    """Ensure a required text field isn't empty."""
    if value is None or value == "":
        raise ValueError(f"{field_name} is required.")
    cleaned_value = str(value).strip()

    if not cleaned_value:
        raise ValueError(f"{field_name} cannot be empty.")

    return cleaned_value

#It validates the date
def validate_iso_date(value):
    """Validate a date written in YYYY-MM-DD format"""
    if not isinstance(value, str):
        raise ValueError("Date must be a string.")

    try:
        parsed_date = date.fromisoformat(value)
    except ValueError:
        raise ValueError("Invalid date format.")

    if parsed_date.isoformat() != value:
        raise ValueError("Date must use YYYY-MM-DD format.")

    return value

#It validates the priority column
def validate_priority(value):
    """Accept only low,medium or high priority."""
    if not isinstance(value, str):
        raise ValueError("Priority must be low, medium, or high.")

    priority = value.strip().lower()

    if priority not in ("low", "medium", "high"):
        raise ValueError("Priority must be low, medium, or high.")

    return priority

#it validates a transaction type
def validate_transaction_type(value):
    """Accept only income or expense transactions"""
    if not isinstance(value, str):
        raise ValueError("Type must be income or expense.")
    transaction_type = value.strip().lower()
    if transaction_type not in ("income", "expense"):
        raise ValueError("Type must be income or expense.")
    return transaction_type

#It validates a amount
def validate_amount(value):
    """Ensure an amount is numeric,finite and greater than zero."""
    import math

    try:
        amount = float(value)
    except (ValueError, TypeError):
        raise ValueError("Amount must be a valid number.")
    if not math.isfinite(amount) or amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    return amount
 