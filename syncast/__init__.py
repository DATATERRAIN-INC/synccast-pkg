"""
syncast
-------

Python SDK for interacting with the SyncCast real-time messaging system.

Provides:
- SDK-style access via `from syncast.sdk import syncast`
- Versioning and configuration placeholders
"""

from typing import Optional

# Version
from syncast._version import VERSION as __version__

# Global configuration placeholders (can be set dynamically or via the SDK)
app_id: Optional[str] = None
app_secret: Optional[str] = None
api_base: str = "https://synccast.socialroots-test.net"

__all__ = [
    "__version__",
    "app_id",
    "app_secret",
    "api_base",
]
