# syncast/core/enums.py

from enum import Enum, IntEnum

class SyncCastEventType(str, Enum):
    """Types of real-time SyncCast notifications."""
    SYSTEM_EVENT = "system"
    PUSH_ALERT = "push"
    USER_PRESENCE = "presence"
    DATA_SYNC = "data"
    CHAT_MESSAGE = "message"
    USER_TYPING = "typing"
    ROOM_UPDATE = "room"


class SyncCastPriorityLevel(str, Enum):
    """Defines importance level for notifications."""
    LOW = "low"            # Background or low-urgency
    MEDIUM = "normal"      # Default importance
    HIGH = "high"          # Critical / urgent

class SyncCastQosLevel(IntEnum):
    """MQTT Quality of Service levels."""
    FIRE_AND_FORGET = 0     # At most once: Fast, unreliable
    DELIVER_AT_LEAST_ONCE = 1  # Guaranteed delivery, may duplicate
    DELIVER_EXACTLY_ONCE = 2   # Most reliable, no duplicates