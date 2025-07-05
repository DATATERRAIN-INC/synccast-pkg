# syncast/exceptions/__init__.py

"""
SyncCast Exception Interface

Centralized import hub for all SyncCast-specific exceptions.
These cover API errors, validation failures, topic or dispatch issues,
and specialized error categories for presence, payloads, and more.

Usage:
    from syncast.exceptions import SyncCastAPIError, SyncCastErrorCode
"""

# ── Base Error ────────────────────────────────────────────────────────────
from .base import SyncCastError                     # Root exception for all SyncCast errors

# ── Error Codes ─────────────────────────────────────────────────────────────────
from .codes import SyncCastErrorCode                # Enum for standardized error codes

# ── Specific Exception Types ────────────────────────────────────────────────────
from .types import (
    SyncCastAPIError,                               # Raised when an API call fails
    SyncCastTopicError,                             # Raised for invalid or unresolved topics
    SyncCastPayloadError,                           # Raised for payload structure/validation issues
    SyncCastDispatchError,                          # Raised when dispatching to API fails
    SyncCastValidationError,                        # Raised for bad input validation
    SyncCastPresenceError,                          # Raised on presence state violations
)

__all__ = [
    "SyncCastError",
    "SyncCastErrorCode",
    "SyncCastAPIError",
    "SyncCastTopicError",
    "SyncCastPayloadError",
    "SyncCastDispatchError",
    "SyncCastValidationError",
    "SyncCastPresenceError"
]
