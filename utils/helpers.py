from datetime import date, datetime, timedelta

#it gets today's date
def get_today():
    """Return today's date as YYYY-MM-DD"""
    return date.today().isoformat()

#it gets tommorow's date
def get_tomorrow():
    """Return tomorroe's date as YYYY-MM-DD"""
    tommorow = date.today() + timedelta(days=1)
    return tommorow.isoformat()

#it gets the date after a specific date
def get_date_after_days(days):
    """Return the date after the given number of days."""
    future_date = date.today() + timedelta(days=days)
    return future_date.isoformat()

#it gets the current month
def get_current_month():
    """Return the current month as YYYY-MM"""
    return date.today().strftime("%Y-%m")

#check whtehter a date is valid
def is_valid_iso_date(value):
    """Check whether a date uses YYYY-MM-DD and is a real date."""
    try:
        date.fromisoformat(value)
        return True
    except (ValueError, TypeError):
        return False

#It formats a date in the correct format
def format_date(value, output_format="%Y-%m-%d"):
    """Convert YYYY-MM-DD into a more readable date."""
    if not value:
        return ""

    try:
        parsed_date = date.fromisoformat(value)
        return parsed_date.strftime(output_format)
    except (ValueError, TypeError):
        return value

#it formats currency
def format_currency(amount, currency_symbol="₹"):
    """Format a number as currency with commas and two decimal places."""    
    try:
        amount = float(amount)
        return f"{currency_symbol}{amount:,.2f}"
    except (ValueError, TypeError):
        raise ValueError("Amount must be a valid number.")

#it turns a number into a percentage
def format_percentage(value, decimal_places=1):
    """Format a number as a percentage"""
    try:
        value = float(value)
        return f"{value: {decimal_places}f}%"
    except (ValueError, TypeError):
        raise ValueError("Percentage must be a valid number.")

#it just normalize the text by cutting extr space
def normalize_text(value):
    """Remove extra spaces and normalize text for searching"""
    if value is None:
        return ""
    return " ".join(str(value).split())

#it gets the status of a task
def get_task_status(due_date, completed=0):
    """Determine a task's status from its completionand due date."""
    if completed:
        return "Completed"
    if not due_date:
        return "No due date"
    if not is_valid_iso_date(due_date):
        return "Invalid date"
    task_date = date.fromisoformat(due_date)
    today = date.today()

    if task_date < today:
        return "Overdue"
    elif task_date == today:
        return "Due today"
    else:
        return "Upcoming"

#check is a task is overdue
def is_task_overdue(due_date, completed=0):
    """Return True if an unfinished task is overdue."""
    return get_task_status(due_date, completed) == "Overdue"

#gets days until task due
def get_days_until_due(due_date):
    """Return days until the due date, or None for an invalid date."""
    if not is_valid_iso_date(due_date):
        return None

    task_date = date.fromisoformat(due_date)
    return (task_date - date.today()).days
