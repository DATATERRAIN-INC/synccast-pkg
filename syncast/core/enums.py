# syncast/core/enums.py

# Default package imports
from enum import Enum, IntEnum
class SyncCastEventType(str, Enum):
    """Types of real-time SyncCast notifications."""
    SYSTEM_EVENT = "system"        # Internal system-level events (e.g. maintenance, config updates)
    PUSH_ALERT = "push"            # Push notifications triggered by alerts or actions
    USER_PRESENCE = "presence"     # Real-time presence updates (online/offline/away)
    DATA_SYNC = "data"             # Data synchronization events (e.g. cache, model sync)
    CHAT_MESSAGE = "message"       # New chat messages (1:1, group, or broadcast)
    USER_TYPING = "typing"         # Typing indicators (user is typing in a chat/room)
    ROOM_UPDATE = "room"           # Room-related events (e.g. name change, participant list update)
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