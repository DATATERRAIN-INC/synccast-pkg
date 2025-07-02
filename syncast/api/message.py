from typing import Optional, Dict, Any, Union

from syncast.core.dispatcher import SyncCastDispatcher
from syncast.core.topic import SyncCastTopicBuilder
from syncast.core.payload import SyncCastPayloadBuilder
from syncast.core.enums import SyncCastEventType
from syncast.core.endpoints import PushEndpoints
from syncast.models import SyncCastScope


class MessageService:
    """
    Service for dispatching chat messages over SyncCast.
    """

    def __init__(self, dispatcher: SyncCastDispatcher, app_id: str):
        self.dispatcher = dispatcher
        self.app_id = app_id  # used for topic generation

    def send_message(
        self,
        *,
        user_id: str,
        data: Dict[str, Any],
        scope: Union[str, SyncCastScope] = "chat",
        channel: str = "message",
        topic: Optional[str] = None,
        room_id: Optional[str] = None,
        sender_name: Optional[str] = None,
        sender_role: Optional[str] = None,
        platform: Optional[str] = None,
        device: Optional[str] = None,
        location: Optional[str] = None,
    ) -> dict:
        """
        Send a chat message via MQTT through SyncCast.

        Args:
            user_id (str): The sender's user ID.
            data (dict): Message payload (e.g., {"text": "Hello"}).
            scope (Union[str, SyncCastScope]): The message scope.
            channel (str): Channel name (default: "message").
            topic (Optional[str]): Custom topic override.
            room_id (Optional[str]): Optional room context.
            sender_name (Optional[str]): Display name.
            sender_role (Optional[str]): Sender role.
            platform/device/location: Metadata for context.

        Returns:
            dict: Dispatcher response.
        """
        # Dynamically build topic if not passed
        if not topic:
            builder = SyncCastTopicBuilder(app_id=self.app_id, scope=scope).channel(channel)
            if room_id:
                builder.extra(room_id)
            topic = builder.for_user(user_id).build()

        # Build payload
        payload_builder = (
            SyncCastPayloadBuilder(user=user_id, type=SyncCastEventType.CHAT_MESSAGE)
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

        return self.dispatcher.post(PushEndpoints.MESSAGE, json=payload_builder.build())
