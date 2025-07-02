from syncast.exceptions.base import SyncCastError
from syncast.exceptions.codes import SyncCastErrorCode

class SyncCastPresenceError(SyncCastError):
    """
    Raised when a presence-related operation fails.
    
    Examples:
        - Presence tracking logic error.
        - Invalid presence state update.
    """
    def __init__(self, message="Presence tracking error", extra=None):
        super().__init__(message, code=SyncCastErrorCode.PRESENCE_ERROR, extra=extra)