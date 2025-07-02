# syncast/core/constants.py

from enum import Enum, IntEnum

class NotificationType(str, Enum):
    """Represents different types of notifications."""
    SYSTEM = "system"
    PUSH = "push"
    PRESENCE = "presence"
    DATA = "data"
    MESSAGE = "message"
    TYPING = "typing"
    ROOM = "room"

class NotificationPriority(str, Enum):
    """Defines priority levels for notifications."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class QosLevel(IntEnum):
    """Quality of Service levels for MQTT delivery."""
    AT_MOST_ONCE = 0      # Fire and forget
    AT_LEAST_ONCE = 1     # Guaranteed delivery, may be duplicate
    EXACTLY_ONCE = 2      # Guaranteed one-time delivery
