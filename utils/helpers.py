"""
Utility functions for the Inventory Management System
"""

from datetime import datetime, timedelta
import re


def validate_email(email: str) -> bool:
    """Validate email format"""
    if not email:
        return True  # Email is optional
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate phone format"""
    if not phone:
        return True  # Phone is optional
    # Allow various phone formats
    pattern = r'^[\d\s\-\+\(\)]+$'
    return re.match(pattern, phone) is not None


def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"${amount:,.2f}"


def format_date(date_str: str) -> str:
    """Format date string to readable format"""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return date_obj.strftime("%Y-%m-%d %I:%M %p")
    except:
        return date_str


def get_date_range(days: int) -> tuple:
    """Get start and end date for last N days"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


def validate_positive_number(value, field_name: str) -> tuple:
    """Validate that a value is a positive number"""
    try:
        num = float(value)
        if num < 0:
            return False, f"{field_name} cannot be negative"
        return True, num
    except ValueError:
        return False, f"{field_name} must be a valid number"


def validate_positive_integer(value, field_name: str) -> tuple:
    """Validate that a value is a positive integer"""
    try:
        num = int(value)
        if num < 0:
            return False, f"{field_name} cannot be negative"
        return True, num
    except ValueError:
        return False, f"{field_name} must be a valid integer"
