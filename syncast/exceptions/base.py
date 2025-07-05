# Default package imports
from typing import Optional, Dict

# SyncCast custom exceptions error code
from syncast.exceptions.codes import SyncCastErrorCode

class SyncCastError(Exception):
    """
    Base exception class for all SyncCast-related errors.

    Attributes:
        message (str): A human-readable error message.
        code (str): A string error code (e.g., 'TOPIC_ERROR', 'PAYLOAD_ERROR').
        extra (dict): Optional additional details for debugging or error response.

    Methods:
        to_dict(): Returns a structured dictionary representation of the error.
    """

    def __init__(
        self,
        message: str,
        code: str = SyncCastErrorCode.API_ERROR,
        extra: Optional[Dict[str, any]] = None
    ):
        self.message = message
        self.code = code
        self.extra = extra or {}
        super().__init__(f"[{self.code}] {self.message}")

    def to_dict(self) -> Dict[str, any]:
        """
        Returns a serializable representation of the error.
        Useful for API responses or logging.
        """
        return {
            "error": self.code,
            "message": self.message,
            "details": self.extra,
        }
