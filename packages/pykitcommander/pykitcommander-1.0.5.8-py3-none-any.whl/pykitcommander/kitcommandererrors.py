"""
Exceptions/Errors that pykitcommander can raise
"""

class PykitcommanderError(Exception):
    """
    Base class for all Pykitcommander specific exceptions
    """

    def __init__(self, msg=None, code=0):
        super(PykitcommanderError, self).__init__(msg)
        self.code = code

class PortError(PykitcommanderError):
    """
    Port connection failure
    """
    def __init__(self, msg=None):
        super(PortError, self).__init__(msg)
        self.msg = msg

class KitError(PykitcommanderError):
    """
    Kit failure
    """
    def __init__(self, msg=None):
        super(KitError, self).__init__(msg)
        self.msg = msg

class KitConnectionError(PykitcommanderError):
    """
    Kit connection failure
    """
    def __init__(self, value, msg=None):
        super(KitConnectionError, self).__init__(msg)
        self.value = value
        self.msg = msg

    def __str__(self):
        return repr(self.value)

class KitCommunicationError(PykitcommanderError):
    """
    Error when sending command or receiving response
    """
    def __init__(self, msg=None):
        super(KitCommunicationError, self).__init__(msg)
        self.msg = msg
