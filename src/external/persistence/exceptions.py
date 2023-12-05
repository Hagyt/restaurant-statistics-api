class OperationalException(Exception):

    def __init__(self, message: str = None):
        super(OperationalException, self).__init__(message)