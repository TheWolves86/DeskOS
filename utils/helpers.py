from datetime import date, datetime, timedelta

def get_today():
    """Return today's date as YYYY-MM-DD"""
    return date.today().isoformat()

def get_tomorrow():
    """Return tomorroe's date as YYYY-MM-DD"""
    tommorow = date.today() + timedelta(days=1)
    return tommorow.isoformat()

def get_date_after_days(days):
    """Return the date after the given number of days."""
    future_date = date.today() + timedelta(days=days)
    return future_date.isoformat()

def get_current_month():
    """Return the current month as YYYY-MM"""
    return date.today().strftime("%Y-%m")

def is_valid_iso_date(value):
    """Check whether a date uses YYYY-MM-DD and is a real date."""
    try:
        date.fromisoformat(value)
        return True
    except (ValueError, TypeError):
        return False

def format_date(value, output_format="%Y-%m-%d"):
    """Convert YYYY-MM-DD into a more readable date."""
    if not value:
        return ""

    try:
        parsed_date = date.fromisoformat(value)
        return parsed_date.strftime(output_format)
    except (ValueError, TypeError):
        return value

def format_currency(amount, currency_symbol="₹"):
    """Format a number as currency with commas and two decimal places."""    
    try:
        amount = float(amount)
        return f"{currency_symbol}{amount:,.2f}"
    except (ValueError, TypeError):
        raise ValueError("Amount must be a valid number.")

def format_percentage(value, decimal_places=1):
    """Format a number as a percentage"""
    try:
        value = float(value)
        return f"{value: {decimal_places}f}%"
    except (ValueError, TypeError):
        raise ValueError("Percentage must be a valid number.")

def normalize_text(value):
    """Remove extra spaces and normalize text for searching"""
    if value is None:
        return ""
    return " ".join(str(value).split())

