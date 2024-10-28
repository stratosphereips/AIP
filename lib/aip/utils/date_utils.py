import logging
from datetime import datetime


def validate_and_convert_date(date_str):
    """
    Validates a date string in 'YYYY-MM-DD' format and converts it to a date object.
    """
    try:
        dateobj = datetime.strptime(date_str, '%Y-%m-%d')
        return dateobj.date()
    except ValueError as e:
        logging.error(f"Invalid date format for '{date_str}', expected YYYY-MM-DD")
        raise ValueError(f"Invalid date format: {date_str}, expected YYYY-MM-DD") from e