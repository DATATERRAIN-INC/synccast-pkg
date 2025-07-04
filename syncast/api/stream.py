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
        event_type: SyncCastEventType = SyncCastEventType.DATA_SYNC,
        scope: Union[str, AbstractSyncCastScope] = "ui",
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
        """

        try:
            # Build topic if not provided
            if not topic:
                builder = SyncCastTopicBuilder(app_id=self.app_id, scope=scope).channel(channel)
                if target_id:
                    builder.extra(target_id)
                topic = builder.for_user(user_id).build()

            # Build payload
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

            payload = payload_builder.build()

            # Send to SyncCast
            return self.dispatcher.post(PushEndpoints.SYNC, json=payload)

        except (ValueError, SyncCastTopicError) as e:
            raise SyncCastTopicError(
                message="Invalid topic during UI sync",
                extra={"scope": str(scope), "channel": channel, "target_id": target_id}
            ) from e

        except SyncCastPayloadError as e:
            raise SyncCastPayloadError(
                message="Invalid UI sync payload",
                extra={"user_id": user_id, "topic": topic}
            ) from e

        except SyncCastDispatchError as e:
            raise  # Already wrapped with dispatch metadata

        except Exception as e:
            raise SyncCastAPIError(
                message="Unexpected error while sending UI update",
                extra={"user_id": user_id, "topic": topic, "error": str(e)}
            ) from e
