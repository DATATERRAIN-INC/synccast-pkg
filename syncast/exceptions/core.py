from syncast.exceptions.base import SyncCastError
from syncast.exceptions.codes import SyncCastErrorCode

class SyncCastTopicError(SyncCastError):
    """
    Raised when an error occurs during topic construction or validation.
    
    Examples:
        - Invalid channel name for a given scope.
        - Missing topic components.
    """
    def __init__(self, message="Invalid topic", extra=None):
        super().__init__(message, code=SyncCastErrorCode.TOPIC_ERROR, extra=extra)

class SyncCastPayloadError(SyncCastError):
    """
    Raised when the payload being constructed is invalid or incomplete.
    
    Examples:
        - Missing required payload fields (e.g., user_id, topic).
        - Unsupported payload structure or data.
    """
    def __init__(self, message="Invalid payload", extra=None):
        super().__init__(message, code=SyncCastErrorCode.PAYLOAD_ERROR, extra=extra)

class SyncCastDispatchError(SyncCastError):
    """
    Raised when the dispatcher fails to send the payload to the broker or API.
    
    Examples:
        - HTTP/MQTT request failure.
        - Connection timeout or invalid endpoint.
    """
    def __init__(self, message="Dispatcher failed", extra=None):
        super().__init__(message, code=SyncCastErrorCode.DISPATCH_ERROR, extra=extra)
