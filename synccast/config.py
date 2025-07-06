"""
synccast.config

Module for storing global configuration values for SyncCast SDK.

These values are intended to be updated only internally by the SDK instance,
and accessed (read-only) by other parts of the package.

This prevents accidental external modification while allowing global visibility.
"""

from typing import Optional

# Private variables for internal storage of credentials
_app_id: Optional[str] = None
_app_secret: Optional[str] = None

# API base URL can be read-only and fixed here
_api_base: str = "https://synccast.socialroots-test.net"


def get_app_id() -> Optional[str]:
    """
    Get the current global app_id.

    Returns:
        Optional[str]: The app_id if set, otherwise None.
    """
    return _app_id


def get_app_secret() -> Optional[str]:
    """
    Get the current global app_secret.

    Returns:
        Optional[str]: The app_secret if set, otherwise None.
    """
    return _app_secret


def get_api_base() -> str:
    """
    Get the base URL for SyncCast API.

    Returns:
        str: The API base URL.
    """
    return _api_base
