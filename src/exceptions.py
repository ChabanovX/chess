class OutOfBoundsException(Exception):
    """Exception raised when a click is out of the board's bounds."""
    def __init__(self, message="Click was out of bounds"):
        self.message = message
        super().__init__(self.message)
        

