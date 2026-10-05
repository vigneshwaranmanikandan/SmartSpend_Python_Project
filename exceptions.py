class SmartSpendError(Exception):
    """Base exception for SmartSpend."""


class InvalidExpenseError(SmartSpendError):
    """Raised when an expense is invalid."""


class ExpenseNotFoundError(SmartSpendError):
    """Raised when an expense ID does not exist."""
