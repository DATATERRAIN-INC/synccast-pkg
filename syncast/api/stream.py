from typing import Optional, Dict, Any, Union

from syncast.core.dispatcher import SyncCastDispatcher
from syncast.core.topic import SyncCastTopicBuilder
from syncast.core.payload import SyncCastPayloadBuilder
from syncast.core.enums import SyncCastEventType
from syncast.core.endpoints import DataEndpoints
from syncast.models import SyncCastScope


class StreamService:
    """
    Service for pushing UI update events (e.g., real-time data refreshes) via SyncCast.
    """

    def __init__(self, dispatcher: SyncCastDispatcher, app_id: str):
        self.dispatcher = dispatcher
        self.app_id = app_id

    def send_update(
        self,
        *,
        user_id: str,
        data: Dict[str, Any],
        event_type: SyncCastEventType = SyncCastEventType.UI_DATA_SYNC,
        scope: Union[str, SyncCastScope] = "ui",
        channel: str = "sync",
        topic: Optional[str] = None,
        target_id: Optional[str] = None,
        sender_name: Optional[str] = None,
        sender_role: Optional[str] = None,
        platform: Optional[str] = None,
        device: Optional[str] = None,
        location: Optional[str] = None,
    ) -> dict:
        """
        Send a real-time UI data sync event.

        Args:
            user_id (str): User ID to whom the update is sent.
            data (dict): Payload data.
            event_type (SyncCastEventType): Event type (defaults to UI_DATA_SYNC).
            scope (str|SyncCastScope): MQTT scope (can be string or model).
            channel (str): Channel (default "sync").
            topic (str): Optional override for topic.
            target_id (str): Optional additional identifier (like screen or component).
            sender_name (str): Optional sender name.
            sender_role (str): Optional sender role.
            platform/device/location (Optional[str]): Optional metadata.

        Returns:
            dict: Response from dispatcher.
        """
        if not topic:
            builder = SyncCastTopicBuilder(app_id=self.app_id, scope=scope).channel(channel)
            if target_id:
                builder.extra(target_id)
            topic = builder.for_user(user_id).build()

        payload_builder = (
            SyncCastPayloadBuilder(user=user_id, type=event_type)
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

        return self.dispatcher.post(DataEndpoints.SYNC, json=payload_builder.build())
