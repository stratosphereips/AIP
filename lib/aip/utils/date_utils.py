from datetime import datetime
from datetime import date


def validate_and_convert_date(date_str):
    """
    Validates a date string in 'YYYY-MM-DD' format and converts it to a date object.
    """
    try:
        dateobj = datetime.strptime(date_str, '%Y-%m-%d').date()
        date_today = date.today()
        if dateobj > date_today:
            raise ValueError(f"The input date '{date_str}' cannot be in the future.")
        return dateobj
    except ValueError as err:
        raise ValueError(f"Invalid date format: {date_str}, expected YYYY-MM-DD") from err