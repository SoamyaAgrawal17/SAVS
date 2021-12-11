class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class AuthError(Error):
    """Exception raised for errors in the authentication.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message, status):
        self.message = message
        self.status = status


'''
The class skeleton is adapted from
https://docs.python.org/3/tutorial/errors.html
'''
