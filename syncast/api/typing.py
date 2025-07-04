from typing import Optional, Dict, Any, Union

from syncast.core.dispatcher import SyncCastDispatcher
from syncast.core.topic import SyncCastTopicBuilder
from syncast.core.payload import SyncCastPayloadBuilder
from syncast.core.enums import SyncCastEventType
from syncast.core.endpoints import PushEndpoints
from syncast.models import AbstractSyncCastScope


from typing import Optional, Dict, Any, Union
from syncast.core.dispatcher import SyncCastDispatchError
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


class TypingService:
    """
    Service for dispatching typing status updates over SyncCast.
    """

    def __init__(self, dispatcher: SyncCastDispatcher, app_id: str):
        self.dispatcher = dispatcher
        self.app_id = app_id

    def send_typing(
        self,
        *,
        user_id: str,
        data: Dict[str, Any],
        scope: Union[str, AbstractSyncCastScope] = "chat",
        channel: str = "typing",
        topic: Optional[str] = None,
        room_id: Optional[str] = None,
        sender_name: Optional[str] = None,
        sender_role: Optional[str] = None,
        platform: Optional[str] = None,
        device: Optional[str] = None,
        location: Optional[str] = None,
    ) -> dict:
        """
        Send typing event to the SyncCast system.
        """

        try:
            # Topic generation
            if not topic:
                builder = SyncCastTopicBuilder(app_id=self.app_id, scope=scope).channel(channel)
                if room_id:
                    builder.extra(room_id)
                topic = builder.for_user(user_id).build()

            # Payload creation
            payload_builder = (
                SyncCastPayloadBuilder(user=user_id, type=SyncCastEventType.USER_TYPING)
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

            # Send via dispatcher
            return self.dispatcher.post(PushEndpoints.TYPING, json=payload)

        except (ValueError, SyncCastTopicError) as e:
            raise SyncCastTopicError("Failed to generate topic", extra={"scope": str(scope), "room_id": room_id}) from e

        except SyncCastPayloadError as e:
            raise SyncCastPayloadError("Invalid typing payload", extra={"user_id": user_id, "topic": topic}) from e

        except SyncCastDispatchError as e:
            raise  # already a dispatch-level error with context

        except Exception as e:
            raise SyncCastAPIError(
                "Unexpected error while sending typing event",
                extra={"error": str(e), "user_id": user_id, "topic": topic}
            ) from e
