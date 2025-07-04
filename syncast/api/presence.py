from typing import Optional, Dict, Any, Union

from syncast.core.dispatcher import SyncCastDispatcher
from syncast.core.topic import SyncCastTopicBuilder
from syncast.core.payload import SyncCastPayloadBuilder
from syncast.core.enums import SyncCastEventType
from syncast.core.endpoints import PushEndpoints
from syncast.models import AbstractSyncCastScope

from syncast.exceptions.core import (
    SyncCastTopicError,
    SyncCastPayloadError,
    SyncCastDispatchError,
    SyncCastAPIError
)


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
        scope: Union[str, AbstractSyncCastScope] = "chat",
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
        """

        try:
            # Generate topic
            if not topic:
                builder = SyncCastTopicBuilder(app_id=self.app_id, scope=scope).channel(channel)
                if room_id:
                    builder.extra(room_id)
                topic = builder.for_user(user_id).build()

            # Build payload
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

            payload = payload_builder.build()

            # Dispatch to broker
            return self.dispatcher.post(PushEndpoints.PRESENCE, json=payload)

        except (ValueError, SyncCastTopicError) as e:
            raise SyncCastTopicError(
                message="Failed to build presence topic",
                extra={"scope": str(scope), "channel": channel, "room_id": room_id}
            ) from e

        except SyncCastPayloadError as e:
            raise SyncCastPayloadError(
                message="Invalid presence payload",
                extra={"user_id": user_id, "topic": topic}
            ) from e

        except SyncCastDispatchError:
            raise  # Already carries context from dispatcher

        except Exception as e:
            raise SyncCastAPIError(
                message="Unexpected error while sending presence update",
                extra={"user_id": user_id, "topic": topic, "error": str(e)}
            ) from e
