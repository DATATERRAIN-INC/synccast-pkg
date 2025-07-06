# synccast/models/__init__.py

"""
Abstract base models for SyncCast data structures.

These models define the reusable schema and behaviors for key concepts like
scopes, channels, presence, messages, reactions, and read trackers. Intended to be
subclassed by actual Django models within your project or app.
"""

# ── Core Model Abstractions ─────────────────────────────────────────────────────
from .scope import AbstractSyncCastScope                  # Base for real-time scope types
from .channel import AbstractSyncCastChannel              # Channel names and metadata
from .presence import AbstractSyncCastUserPresence        # Tracks user online/offline status
from .message import AbstractSyncCastMessage              # Core message structure and metadata
from .attachment import AbstractSyncCastAttachment        # Attachments linked to messages
from .reaction import AbstractSyncCastReaction            # Emoji or reaction tracking
from .tracker import AbstractSyncCastReadTracker          # Per-user message read tracking


__all__ = [
    "AbstractSyncCastScope",
    "AbstractSyncCastChannel",
    "AbstractSyncCastUserPresence",
    "AbstractSyncCastMessage",
    "AbstractSyncCastAttachment",
    "AbstractSyncCastReaction",
    "AbstractSyncCastReadTracker",
]
