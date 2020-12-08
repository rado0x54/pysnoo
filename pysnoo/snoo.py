"""The main API class"""


class Snoo:
    """A Python Abstraction object to Snoo Smart Sleeper Bassinett."""
    # pylint: disable=too-few-public-methods

    def __init__(self, auth):
        """Initialize the Snoo object."""
        self.auth = auth
