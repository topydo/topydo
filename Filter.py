class Filter(object):
    # def __init__(self):
    #     pass

    def filter(self, p_todos, p_limit=None):
        """
        Filters a list of todos. Truncates the list after p_limit todo
        items (or no maximum limit if omitted).
        """

        result = [t for t in p_todos if self.match(t)]
        return result[:p_limit]

    def match(self, p_todo):
        """ Default match value. """
        return True

class GrepFilter(Filter):
    """ Matches when the todo text contains a text. """

    def __init__(self, p_expression, p_case_sensitive=None):
        self.expression = p_expression

        if p_case_sensitive:
            self.case_sensitive = p_case_sensitive
        else:
            # only be case sensitive when the expression contains at least one
            # capital character.
            self.case_sensitive = \
                len([c for c in p_expression if c.isupper()]) > 0

    def match(self, p_todo):
        expr = self.expression
        string = p_todo.source()
        if not self.case_sensitive:
            expr = expr.lower()
            string = string.lower()

        return string.find(expr) != -1

class RelevanceFilter(Filter):
    """
    Matches when the todo is relevant, i.e.:

    The item has not been completed AND
    The start date is blank, today or in the past, AND
    The priority is 'A' or the priority is B with due date within 30 days or
    the priority is C with due date within 14 days.
    """

    def match(self, p_todo):
        is_due = p_todo.is_active()
        is_due |= p_todo.due_date() == None
        is_due |= p_todo.priority() == 'A'
        is_due |= p_todo.priority() == 'B' and p_todo.days_till_due() <= 30
        is_due |= p_todo.priority() == 'C' and p_todo.days_till_due() <= 14

        return p_todo.is_active() and is_due
