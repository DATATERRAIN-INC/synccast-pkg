import syncast

class SyncCastRequestConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SyncCastRequestConfig, cls).__new__(cls)
        return cls._instance

    @property
    def base_url(self) -> str:
        return syncast.api_base

    @property
    def app_id(self) -> str:
        return syncast.app_id

    @property
    def app_secret(self) -> str:
        return syncast.app_secret

    def as_dict(self) -> dict:
        return {
            "base_url": self.base_url,
            "app_id": self.app_id,
            "app_secret": "***" if self.app_secret else None,
        }

    def is_configured(self) -> bool:
        return bool(self.app_id and self.app_secret)
    

config = SyncCastRequestConfig()

 
