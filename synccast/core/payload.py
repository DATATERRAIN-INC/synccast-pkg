# Package imports
from typing import Optional, Dict, Any, Union

# SyncCast abstract model
from synccast.models import AbstractSyncCastScope

# SyncCast enums
from synccast.core.enums import (
    SyncCastEventType, 
    SyncCastPriorityLevel, 
    SyncCastQosLevel
)

# SyncCast custom exceptions
from synccast.exceptions.types import SyncCastPayloadError

class SyncCastPayloadBuilder:
    """
    Builds structured notification payloads for SyncCast events.
    Allows setting sender info, core data, metadata, and actions.
    """

    def __init__(
        self,
        user: Optional[Union[int, str]] = None,
        type: SyncCastEventType = SyncCastEventType.PUSH_ALERT,
        priority: SyncCastPriorityLevel = SyncCastPriorityLevel.MEDIUM,
        qos: SyncCastQosLevel = SyncCastQosLevel.DELIVER_AT_LEAST_ONCE
    ) -> None:
        self.user: Optional[str] = str(user) if user is not None else None
        self.type: SyncCastEventType = type
        self.priority: SyncCastPriorityLevel = priority
        self.qos: SyncCastQosLevel = qos
        self.scope: Optional[str] = None
        self.data: Dict[str, Any] = {}
        self.topic: Optional[str] = None
        self.sender_info: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {}
        self.action: Dict[str, str] = {}

    def set_sender_info(self, sender_id: str, sender_name: str, sender_role: Optional[str] = None) -> 'SyncCastPayloadBuilder':
        self.sender_info = {
            "id": sender_id,
            "name": sender_name,
            "role": sender_role or "system"
        }
        return self

    def set_data(self, data: Optional[Dict[str, Any]] = None) -> 'SyncCastPayloadBuilder':
        self.data = data or {}
        return self

    def set_topic(self, topic: str) -> 'SyncCastPayloadBuilder':
        if not topic or not isinstance(topic, str):
            raise SyncCastPayloadError(
                message="Invalid topic format",
                extra={"provided": topic}
            )
        self.topic = topic
        return self

    def set_scope(self, scope: Union[AbstractSyncCastScope, str]) -> 'SyncCastPayloadBuilder':
        if isinstance(scope, AbstractSyncCastScope):
            self.scope = scope.name
        elif isinstance(scope, str):
            self.scope = scope
        else:
            raise SyncCastPayloadError(
                message="Scope must be a string or SyncCastScope instance",
                extra={"provided_type": type(scope).__name__}
            )
        return self

    def set_metadata(self, platform: str, device: str, location: str) -> 'SyncCastPayloadBuilder':
        self.metadata = {
            "platform": platform,
            "device": device,
            "location": location
        }
        return self

    def set_action(self, action_type: str, url: str) -> 'SyncCastPayloadBuilder':
        self.action = {
            "type": action_type,
            "url": url
        }
        return self

    def build(self) -> Dict[str, Any]:
        if not self.topic:
            raise SyncCastPayloadError(
                message="Payload missing required 'topic'",
                extra={"scope": self.scope, "user": self.user}
            )

        return {
            "user_id": self.user,
            "type": self.type.value,
            "priority": self.priority.value,
            "qos": self.qos.value,
            "scope": self.scope,
            "topic": self.topic,
            "data": self.data,
            "sender": self.sender_info,
            "metadata": self.metadata,
            "action": self.action
        }

    def __str__(self):
        return str(self.build())