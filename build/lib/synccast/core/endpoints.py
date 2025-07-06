# synccast/core/endpoints.py

from typing import Final

class PushEndpoints:
    """
    Static definitions for all SyncCast real-time push API endpoints.

    These endpoints are used internally by SyncCastDispatcher and service classes
    to publish real-time events such as messages, typing indicators, presence updates, etc.

    Each constant maps to a backend route that accepts a specific payload format.
    """

    SYSTEM: Final[str] = "/api/chat/system/"          # Internal system event pushes
    TYPING: Final[str] = "/api/chat/typing/"          # User typing state
    MESSAGE: Final[str] = "/api/chat/messages/"       # Chat message delivery
    PRESENCE: Final[str] = "/api/chat/presence/"      # Online/offline presence updates
    NOTIFICATION: Final[str] = "/api/chat/notification/"  # App-level notifications (e.g. alerts)
    SYNC: Final[str] = "/api/chat/sync/"              # UI or client sync triggers (e.g. refresh data)
