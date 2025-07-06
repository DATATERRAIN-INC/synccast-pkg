# synccast/core/__init__.py

"""
Core components for the SyncCast SDK.

This module provides low-level building blocks for topic generation, payload
construction, HTTP dispatching, and endpoint management. These are used by
higher-level service layers like `NotificationService`, `MessageService`, etc.

Typical usage:
    from synccast.core import SyncCastTopicBuilder, SyncCastDispatcher
"""

# ── Topic & Payload Builders ───────────────────────────────────────────────────
from .topic import SyncCastTopicBuilder            # Dynamically builds MQTT topic strings
from .payload import SyncCastPayloadBuilder        # Constructs structured payloads for publishing

# ── Dispatching & API Endpoint Utilities ───────────────────────────────────────
from .dispatcher import SyncCastDispatcher         # HTTP client for sending data to SyncCast APIs
from .endpoints import PushEndpoints               # Predefined API endpoint constants

# ── Public API Exposure ────────────────────────────────────────────────────────
__all__ = [
    "SyncCastTopicBuilder",
    "SyncCastPayloadBuilder",
    "SyncCastDispatcher",
    "PushEndpoints",
]
