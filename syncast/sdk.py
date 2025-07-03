from functools import cached_property

from syncast import app_id, app_secret, api_base

class SyncCastSDK:
    def __init__(self):
        self._app_id = app_id
        self._app_secret = app_secret
        self._api_base = api_base

    def set_credentials(self, app_id: str, app_secret: str):
        """
        Set app_id and app_secret at runtime.
        This clears any cached properties like dispatcher, stream, etc.
        """
        self._app_id = app_id
        self._app_secret = app_secret
        self.__dict__.pop("dispatcher", None)
        self.__dict__.pop("stream", None)
        self.__dict__.pop("presence", None)
        self.__dict__.pop("chat", None)
        self.__dict__.pop("notify", None)
        return self   

    @cached_property
    def config(self):
        from syncast.core.config import SyncCastRequestConfig
        return SyncCastRequestConfig()

    @cached_property
    def dispatcher(self):
        from syncast.core.dispatcher import SyncCastDispatcher
        dispatcher = SyncCastDispatcher().with_base_url(self._api_base)
        if self._app_id and self._app_secret:
            dispatcher.with_secret(self._app_id, self._app_secret)
        return dispatcher

    @cached_property
    def stream(self):
        from syncast.api.stream import StreamService
        return StreamService(dispatcher=self.dispatcher, app_id=self._app_id)

    @cached_property
    def presence(self):
        from syncast.api.presence import PresenceService
        return PresenceService(dispatcher=self.dispatcher, app_id=self._app_id)

    @cached_property
    def chat(self):
        from syncast.api.message import MessageService
        return MessageService(dispatcher=self.dispatcher, app_id=self._app_id)

    @cached_property
    def notify(self):
        from syncast.api.notification import NotificationService
        return NotificationService(dispatcher=self.dispatcher, app_id=self._app_id)

    @cached_property
    def topic_builder(self):
        from syncast.core.topic import SyncCastTopicBuilder
        return SyncCastTopicBuilder  # class, not instance

    @cached_property
    def payload_builder(self):
        from syncast.core.payload import SyncCastPayloadBuilder
        return SyncCastPayloadBuilder  # class, not instance


# Singleton instance
syncast = SyncCastSDK()
