from syncast.exceptions.base import SyncCastError
from syncast.exceptions.codes import SyncCastErrorCode

class SyncCastAPIError(SyncCastError):
    """
    Raised when an API error occurs within SyncCast services.
    
    Examples:
        - 4xx or 5xx API response.
        - Unexpected response structure or status code.
    """
    def __init__(self, message="API error", extra=None):
        super().__init__(message, code=SyncCastErrorCode.API_ERROR, extra=extra)

class SyncCastValidationError(SyncCastError):
    """
    Raised when incoming input fails validation checks.
    
    Examples:
        - Required data is missing or of invalid type.
        - Business logic validation failed before dispatch.
    """
    def __init__(self, message="Validation failed", extra=None):
        super().__init__(message, code=SyncCastErrorCode.VALIDATION_ERROR, extra=extra)