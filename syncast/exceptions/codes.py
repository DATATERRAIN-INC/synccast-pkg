from enum import Enum

class SyncCastErrorCode(str, Enum):
    CONFIG_ERROR = "config_error"
    TOPIC_ERROR = "topic_error"
    PAYLOAD_ERROR = "payload_error"
    DISPATCH_ERROR = "dispatch_error"
    API_ERROR = "api_error"
    VALIDATION_ERROR = "validation_error"
    PRESENCE_ERROR = "presence_error"
    NOTIFICATION_ERROR = "notification_error"
    MESSAGE_ERROR = "message_error"
