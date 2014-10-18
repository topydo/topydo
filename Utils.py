"""
Various utility functions.
"""

from datetime import date
import re

def date_string_to_date(p_date):
    """
    Given a date in YYYY-MM-DD, returns a Python date object. Returns None
    if the date is invalid.
    """
    result = None

    if p_date:
        parsed_date = re.match(r'(\d{4})-(\d{2})-(\d{2})', p_date)
        if parsed_date:
            try:
                result = date(
                    int(parsed_date.group(1)), # year
                    int(parsed_date.group(2)), # month
                    int(parsed_date.group(3))  # day
                )
            except ValueError:
                result = None

    return result

class InvalidTodoNumberException(Exception):
    pass

def convert_todo_number(p_number):
    """ Converts a string number to an integer. """
    try:
        p_number = int(p_number)
    except ValueError:
        raise InvalidTodoNumberException

    return p_number

def is_valid_priority(p_priority):
    return re.match(r'^[A-Z]$', p_priority) != None
