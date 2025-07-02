"""
syncast
-------

Python client for interacting with the SyncCast real-time messaging and notification system.

This module provides:
- Global configuration variables
- A default dispatcher for HTTP/MQTT requests
- Topic and payload builders for structured publishing
- A config interface to access runtime settings
"""

from typing import Optional

# Import version string from internal version module
from syncast._version import VERSION as __version__

# ------------------------------------------------------------------------------
# Default constants for base configuration
# ------------------------------------------------------------------------------

DEFAULT_API_BASE: str = "https://api.syncast.com/v1"

# Core credentials (can be set by the user)
app_id: Optional[str] = None
app_secret: Optional[str] = None

# Retry configuration
max_network_retries: int = 3

# API base URL (can be overridden)
api_base: str = DEFAULT_API_BASE

# ------------------------------------------------------------------------------
# Core interfaces exposed to users
# ------------------------------------------------------------------------------

# Dispatcher handles HTTP requests with retries, secrets, and auth
from syncast.core.dispatcher import SyncCastDispatcher

# RequestConfig reads values from this module for dynamic access
from syncast.core.config import SyncCastRequestConfig

# ------------------------------------------------------------------------------
# Public interface (convenient preconfigured instances)
# ------------------------------------------------------------------------------

# Shared dispatcher using global api_base and credentials
dispatcher = SyncCastDispatcher().with_base_url(api_base)

# Config reader that dynamically reflects runtime values
config = SyncCastRequestConfig()

# ------------------------------------------------------------------------------
# Public exports for package consumers
# ------------------------------------------------------------------------------

__all__ = [
    "__version__",
    "dispatcher",
    "config",
    "app_id",
    "app_secret",
    "api_base",
    "max_network_retries",
    "SyncCastDispatcher",
    "SyncCastRequestConfig"
]
