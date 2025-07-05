# Default package imports
from typing import Optional, Dict

# SyncCast custom exceptions error & errorcode
from syncast.exceptions.base import SyncCastError
from syncast.exceptions.codes import SyncCastErrorCode

class SyncCastTopicError(SyncCastError):
    """
    Raised when an error occurs during topic construction or validation in SyncCast.

    Typical causes:
        - Attempting to use an invalid or undefined channel for a scope.
        - Missing required topic parts (e.g., scope, channel, user).
        - Dynamic building errors (e.g., malformed topic path).

    Args:
        message (str): A human-readable error message.
        extra (dict, optional): Additional debug context (e.g., scope, channel, valid options).

    Example:
        raise SyncCastTopicError(
            message="Channel 'typingX' not found in scope 'chat'",
            extra={"scope": "chat", "channel": "typingX", "valid_channels": ["typing", "message"]}
        )
    """
    def __init__(self, message: str = "Invalid topic", extra: Optional[dict] = None):
        super().__init__(message, code=SyncCastErrorCode.TOPIC_ERROR, extra=extra)

class SyncCastPayloadError(SyncCastError):
    """
    Raised when the payload being constructed is invalid, incomplete, or malformed.

    Common causes:
        - Missing required fields (e.g., user_id, topic, data).
        - Incorrect payload format or data types.
        - Inconsistent structure with expected SyncCast protocol.

    Args:
        message (str): Description of the payload issue.
        extra (dict, optional): Additional debug information (e.g., payload snapshot, field name).

    Example:
        raise SyncCastPayloadError(
            message="Missing required field: 'topic'",
            extra={"field": "topic", "payload": {...}}
        )
    """
    def __init__(self, message: str = "Invalid payload", extra: Optional[dict] = None):
        super().__init__(message, code=SyncCastErrorCode.PAYLOAD_ERROR, extra=extra)


class SyncCastDispatchError(SyncCastError):
    """
    Raised when the dispatcher fails to send the payload to the broker or API.

    Typical causes:
        - HTTP/MQTT request failures.
        - Connection timeouts.
        - Invalid or unreachable endpoint.
        - Response parsing errors (e.g., non-JSON reply).

    Args:
        message (str): A human-readable message describing the failure.
        extra (dict, optional): Additional metadata (e.g., status code, response body).

    Example:
        raise SyncCastDispatchError(
            message="Failed to POST to SyncCast API",
            extra={"status": 503, "response": "Service Unavailable"}
        )
    """
    def __init__(self, message: str = "Dispatcher failed", extra: Optional[dict] = None):
        super().__init__(message, code=SyncCastErrorCode.DISPATCH_ERROR, extra=extra)


class SyncCastAPIError(SyncCastError):
    """
    Raised when an error occurs while interacting with external or internal APIs
    related to SyncCast.

    Common causes:
        - Non-2xx response from a SyncCast service endpoint.
        - Unexpected response schema or missing fields.
        - Timeout or connection failure.

    Args:
        message (str): Human-readable error message.
        extra (dict, optional): Optional metadata for debugging.

    Example:
        raise SyncCastAPIError(
            message="Failed to fetch topic configuration",
            extra={"url": "https://syncast.io/api/topic", "status_code": 500}
        )
    """
    def __init__(self, message: str = "API error", extra: Optional[Dict] = None):
        super().__init__(message, code=SyncCastErrorCode.API_ERROR, extra=extra)

class SyncCastValidationError(SyncCastError):
    """
    Raised when input data fails validation within SyncCast core logic.

    Common causes:
        - Missing required fields.
        - Incorrect types or malformed values.
        - Business logic rules violated.

    Args:
        message (str): Error description.
        extra (dict, optional): Field-level error context or metadata.

    Example:
        raise SyncCastValidationError(
            message="Missing 'user_id' in payload",
            extra={"field": "user_id", "expected": "non-empty string"}
        )
    """
    def __init__(self, message: str = "Validation failed", extra: Optional[Dict] = None):
        super().__init__(message, code=SyncCastErrorCode.VALIDATION_ERROR, extra=extra)


class SyncCastPresenceError(SyncCastError):
    """
    Raised when a presence-related operation fails within SyncCast.

    Common causes:
        - Failed to track online/offline status.
        - Invalid presence update payload.
        - Presence logic conflict (e.g., duplicate session or invalid state transition).

    Args:
        message (str): Description of the failure.
        extra (dict, optional): Additional context or debugging metadata.

    Example:
        raise SyncCastPresenceError(
            message="User disconnected unexpectedly",
            extra={"user_id": "42", "room_id": "abc123", "last_seen": "2025-06-30T12:34:56Z"}
        )
    """
    def __init__(self, message: str = "Presence tracking error", extra: Optional[Dict] = None):
        super().__init__(message, code=SyncCastErrorCode.PRESENCE_ERROR, extra=extra)