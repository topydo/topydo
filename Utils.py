"""
Various utility functions.
"""

import datetime
import re

def date_string_to_date(p_date):
    """
    Given a date in YYYY-MM-DD, returns a Python date object. Returns None
    if the date is invalid.
    """
    result = None

    parsed_date = re.match(r'(\d{4})-(\d{2})-(\d{2})', p_date)

    if parsed_date:
        try:
            date = datetime.date(
                int(parsed_date.group(1)), # year
                int(parsed_date.group(2)), # month
                int(parsed_date.group(3))  # day
            )

            result = date
        except ValueError:
            pass # just return None

    return result
