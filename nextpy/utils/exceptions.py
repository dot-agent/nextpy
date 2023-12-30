# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Custom Exceptions."""


class InvalidStylePropError(TypeError):
    """Custom Type Error when style props have invalid values."""

    pass


class ImmutableStateError(AttributeError):
    """Raised when a background task attempts to modify state outside of context."""


class LockExpiredError(Exception):
    """Raised when the state lock expires while an event is being processed."""

class MatchTypeError(TypeError):
    """Raised when the return types of match cases are different."""

    pass
