import syncast


class SyncCastRequestConfig:
    """
    SyncCastRequestConfig provides access to runtime configuration
    for the SyncCast Dispatcher and related services.

    It reflects values defined in the root `syncast` package, such as:
    - API base URL
    - App ID
    - App Secret

    You can use this class throughout the package to retrieve consistent
    values without importing the global `syncast` config directly.
    """

    @property
    def base_url(self) -> str:
        """
        Returns the configured base URL for SyncCast API requests.
        """
        return syncast.api_base

    @property
    def app_id(self) -> str:
        """
        Returns the current application ID.
        """
        return syncast.app_id

    @property
    def app_secret(self) -> str:
        """
        Returns the current application secret.
        """
        return syncast.app_secret

    def as_dict(self) -> dict:
        """
        Optional helper to return current config as a dictionary.
        Use this for logging or debugging purposes.
        """
        return {
            "base_url": self.base_url,
            "app_id": self.app_id,
            "app_secret": "***" if self.app_secret else None,
        }

    def is_configured(self) -> bool:
        """
        Returns True if both app_id and app_secret are set.
        """
        return bool(self.app_id and self.app_secret)
