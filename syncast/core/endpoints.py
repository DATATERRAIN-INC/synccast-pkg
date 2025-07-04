# syncast/core/endpoints.py

from typing import Final
 
class PushEndpoints:
    """Endpoints for real-time push events."""
    SYSTEM: Final[str] = "api/chat/system"
    TYPING: Final[str] = "api/chat/typing"
    MESSAGE: Final[str] = "api/chat/messages"
    PRESENCE: Final[str] = "api/chat/presence"
    NOTIFICATION: Final[str] = "api/chat/notification"
    SYNC: Final[str] = "api/chat/sync"



