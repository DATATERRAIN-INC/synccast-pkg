from typing import Optional, Dict, Any, Union
from syncast.core.dispatcher import SyncCastDispatcher
from syncast.core.topic import SyncCastTopicBuilder
from syncast.core.payload import SyncCastPayloadBuilder
from syncast.core.enums import SyncCastEventType
from syncast.core.endpoints import PushEndpoints
from syncast.models import SyncCastScope


class PresenceService:
    """
    Service for dispatching presence status updates over SyncCast.
    """

    def __init__(self, dispatcher: SyncCastDispatcher, app_id: str):
        self.dispatcher = dispatcher
        self.app_id = app_id

    def send_presence(
        self,
        *,
        user_id: str,
        data: Dict[str, Any],
        scope: Union[str, SyncCastScope] = "chat",
        channel: str = "presence",
        room_id: Optional[str] = None,
        topic: Optional[str] = None,
        sender_name: Optional[str] = None,
        sender_role: Optional[str] = None,
        platform: Optional[str] = None,
        device: Optional[str] = None,
        location: Optional[str] = None,
    ) -> dict:
        """
        Send presence event to the SyncCast system.

        Args:
            user_id (str): The ID of the user whose presence is being updated.
            data (dict): Arbitrary data payload (e.g., {"status": "online"}).
            scope (Union[str, SyncCastScope]): Scope instance or slug.
            channel (str): Channel under the scope.
            room_id (Optional[str]): Optional room identifier.
            topic (Optional[str]): Override for topic.
            sender_name (Optional[str]): Display name.
            sender_role (Optional[str]): Role name.
            platform/device/location (Optional[str]): Optional metadata.

        Returns:
            dict: API response from dispatcher.
        """
        if not topic:
            builder = SyncCastTopicBuilder(app_id=self.app_id, scope=scope).channel(channel)
            if room_id:
                builder.extra(room_id)
            topic = builder.for_user(user_id).build()

        payload_builder = (
            SyncCastPayloadBuilder(user=user_id, type=SyncCastEventType.USER_PRESENCE)
            .set_scope(scope)
            .set_topic(topic)
            .set_data(data)
        )

        if sender_name:
            payload_builder.set_sender_info(sender_id=user_id, sender_name=sender_name, sender_role=sender_role)

        if platform or device or location:
            payload_builder.set_metadata(
                platform or "unknown", device or "unknown", location or "unknown"
            )

        return self.dispatcher.post(PushEndpoints.PRESENCE, json=payload_builder.build())
