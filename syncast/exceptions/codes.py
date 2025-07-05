#Default package imports
from enum import Enum
class SyncCastErrorCode(str, Enum):

    """
    Standardized error codes for SyncCast exceptions.

    These codes are used internally across the SyncCast SDK for structured
    error handling, debugging, logging, and API responses.
    """
        
    CONFIG_ERROR = "config_error"             # Misconfigured SDK, missing app ID/secret, etc.
    TOPIC_ERROR = "topic_error"               # Failed to build or resolve MQTT topic
    PAYLOAD_ERROR = "payload_error"           # Malformed or invalid message payload
    DISPATCH_ERROR = "dispatch_error"         # Failure in HTTP dispatch to SyncCast API
    API_ERROR = "api_error"                   # General error from SyncCast backend API
    VALIDATION_ERROR = "validation_error"     # Input or field validation failure
    PRESENCE_ERROR = "presence_error"         # Presence system failure (e.g., unknown user state)
    NOTIFICATION_ERROR = "notification_error" # Notification routing or publishing failure
    MESSAGE_ERROR = "message_error"           # Message sending, saving, or formatting failure