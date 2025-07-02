from syncast.exceptions.codes import SyncCastErrorCode

class SyncCastError(Exception):
    def __init__(self, message: str, code: str = SyncCastErrorCode.API_ERROR, extra: dict = None):
        self.message = message
        self.code = code
        self.extra = extra or {}
        super().__init__(f"[{code}] {message}")

    def to_dict(self) -> dict:
        return {
            "error": self.code,
            "message": self.message,
            "details": self.extra,
        }
