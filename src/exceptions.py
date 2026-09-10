class ShowcaseNotFoundError(Exception):
    """Raised when Enka has no showcase data for the given UID."""
    pass


class EnkaRequestError(Exception):
    """Raised when a request to Enka fails for a reason other than 'not found'."""
    pass