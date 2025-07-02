# syncast/core/endpoints.py

from typing import Final
 
class PushEndpoints:
    """Endpoints for real-time push events."""
    SYSTEM: Final[str] = "/push/system"
    TYPING: Final[str] = "/push/typing"
    MESSAGE: Final[str] = "/push/message"
    REACTION: Final[str] = "/push/reaction"
    PRESENCE: Final[str] = "/push/presence"
    BROADCAST: Final[str] = "/push/broadcast"
    NOTIFICATION: Final[str] = "/push/notification"

class DataEndpoints:
    """Endpoints for structured data delivery."""
    CREATE: Final[str] = "/data/create"
    UPDATE: Final[str] = "/data/update"
    DELETE: Final[str] = "/data/delete"
    SYNC: Final[str] = "/data/sync"
    METADATA: Final[str] = "/data/meta"


class ControlEndpoints:
    """Endpoints for system control, health checks, admin signals."""
    HEARTBEAT: Final[str] = "/control/heartbeat"
    ERROR: Final[str] = "/control/error"
    STATUS: Final[str] = "/control/status"
    PING: Final[str] = "/control/ping"
