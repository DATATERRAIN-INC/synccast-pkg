from typing import Optional, Dict, Any, Union
from syncast.core.dispatcher import SyncCastDispatcher
from syncast.core.topic import SyncCastTopicBuilder
from syncast.core.payload import SyncCastPayloadBuilder
from syncast.core.enums import SyncCastEventType
from syncast.core.endpoints import PushEndpoints
from syncast.models import SyncCastScope  # import the model

class NotificationService:
    """
    Service for dispatching system notifications over SyncCast.
    """

    def __init__(self, dispatcher: SyncCastDispatcher, app_id: str):
        self.dispatcher = dispatcher
        self.app_id = app_id  # required for topic builder

    def send_notification(
        self,
        *,
        user_id: str,
        data: Dict[str, Any],
        scope: Union[str, SyncCastScope] = "system",
        channel: str = "notification",
        topic: Optional[str] = None,
        room_id: Optional[str] = None,
        sender_name: Optional[str] = None,
        sender_role: Optional[str] = None,
        platform: Optional[str] = None,
        device: Optional[str] = None,
        location: Optional[str] = None,
    ) -> dict:
        """
        Send a system-level notification to the SyncCast system.

        Args:
            user_id (str): The ID of the user receiving the notification.
            data (dict): Arbitrary data payload.
            scope (Union[str, SyncCastScope]): Scope instance or slug.
            channel (str): Channel name.
            topic (Optional[str]): Custom topic.
            room_id (Optional[str]): Optional room context.
            sender_name/sender_role/platform/device/location: Metadata.

        Returns:
            dict: API response from dispatcher.
        """
        # Build topic dynamically only if not explicitly passed
        if not topic:
            topic_builder = SyncCastTopicBuilder(app_id=self.app_id, scope=scope).channel(channel)
            if room_id:
                topic_builder.extra(room_id)
            topic = topic_builder.for_user(user_id).build()

        # Build payload
        payload_builder = (
            SyncCastPayloadBuilder(user=user_id, type=SyncCastEventType.SYSTEM_NOTIFICATION)
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

        return self.dispatcher.post(PushEndpoints.SYSTEM, json=payload_builder.build())
