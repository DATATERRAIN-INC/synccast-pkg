# synccast/api/__init__.py

"""
SyncCast API Service Interface

Provides centralized access to all core real-time service classes.
Each service encapsulates a distinct functional domain such as messaging,
notifications, presence tracking, stream management, and typing indicators.

Usage:
    from synccast.api import MessageService, StreamService

    messages = MessageService()
    stream = StreamService()
"""

# ──────────────────────────── API Service Exports ──────────────────────────
# Exposes core real-time service classes under the `synccast.api` namespace.
# Enables clean, centralized, and modular access across SyncCast SDK consumers.

from .message import MessageService  # Messaging: send, edit, retrieve messages
from .notification import NotificationService # Notifications: in-app, system, MQTT delivery
from .presence import PresenceService # Presence: user online/offline/away tracking
from .stream import StreamService # Stream: real-time UI sync between active clients
from .typing import TypingService # Typing: real-time typing indicator events

__all__ = [
    "MessageService",
    "NotificationService",
    "PresenceService",
    "StreamService",
    "TypingService"
]