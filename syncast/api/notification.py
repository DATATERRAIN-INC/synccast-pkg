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
    SyncCastAPIError,
)


class NotificationService:
    """
    Service for dispatching system notifications over SyncCast.
    """

    def __init__(self, dispatcher: SyncCastDispatcher, app_id: str):
        self.dispatcher = dispatcher
        self.app_id = app_id

    def send_notification(
        self,
        *,
        user_id: Optional[str],
        data: Dict[str, Any],
        scope: Union[str, AbstractSyncCastScope] = "system",
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
        """

        try:
            if not topic:
                builder = SyncCastTopicBuilder(app_id=self.app_id, scope=scope).channel(channel)
                if room_id:
                    builder.extra(room_id)
                if user_id:
                    builder.for_user(user_id)
                topic = builder.build()

            payload_builder = (
                SyncCastPayloadBuilder(user=user_id, type=SyncCastEventType.SYSTEM_EVENT)
                .set_scope(scope)
                .set_topic(topic)
                .set_data(data)
            )

            if sender_name and user_id:
                payload_builder.set_sender_info(
                    sender_id=user_id, sender_name=sender_name, sender_role=sender_role
                )

            if platform or device or location:
                payload_builder.set_metadata(
                    platform or "unknown", device or "unknown", location or "unknown"
                )

            payload = payload_builder.build()

            return self.dispatcher.post(PushEndpoints.SYSTEM, json=payload)

        except (ValueError, SyncCastTopicError) as e:
            raise SyncCastTopicError(
                message="Invalid topic for system notification",
                extra={"scope": str(scope), "channel": channel, "room_id": room_id}
            ) from e

        except SyncCastPayloadError as e:
            raise SyncCastPayloadError(
                message="Invalid system notification payload",
                extra={"user_id": user_id, "topic": topic}
            ) from e

        except SyncCastDispatchError:
            raise  # Already wrapped in dispatcher

        except Exception as e:
            raise SyncCastAPIError(
                message="Unexpected error while sending system notification",
                extra={"user_id": user_id, "topic": topic, "error": str(e)}
            ) from e
