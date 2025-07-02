# syncast/core/builder.py

# Package imports
from typing import Optional, Dict, Any, Union, Self
from copy import deepcopy

# Local model imports
from syncast.models.scope import SyncCastScope

class SyncCastTopicBuilder:
    """
    Builds MQTT topic strings dynamically based on app_id, scope, 
    channel, and optional user or extra parts.
    Supports wildcards for subscription.
    """
    def __init__(
        self,
        app_id: str,
        scope: 'SyncCastScope',  # Assume this is a Django model with a `.channels.all()` queryset
    ):
        self.app_id = app_id
        self.scope = scope
        self._channel: Optional[str] = None
        self._extra_parts: list[str] = []
        self._user_id: Optional[Union[int, str]] = None
        self._wildcard: bool = False

    def channel(self, channel_name: str) -> Self:
        if not any(c.name == channel_name for c in self.scope.channels.all()):
            valid_channels = [c.name for c in self.scope.channels.all()]
            raise ValueError(
                f"Channel '{channel_name}' not defined for scope '{self.scope.name}'. "
                f"Available: {valid_channels}"
            )
        self._channel = channel_name
        return self

    def extra(self, *parts: Union[str, int]) -> Self:
        self._extra_parts.extend(str(p) for p in parts)
        return self

    def for_user(self, user_id: Union[int, str]) -> Self:
        self._user_id = user_id
        return self

    def wildcard(self) -> Self:
        self._wildcard = True
        return self

    def full_wildcard(self) -> Self:
        self._extra_parts.append("#")
        return self

    def reset(self) -> Self:
        self._channel = None
        self._extra_parts = []
        self._user_id = None
        self._wildcard = False
        return self

    def clone(self) -> Self:
        return deepcopy(self)

    def build(self) -> str:
        if not self._channel:
            raise ValueError("Channel must be set before building topic")
        parts = [self.app_id, self.scope.name, self._channel] + self._extra_parts
        if self._user_id is not None:
            parts += ["user", "+" if self._wildcard else str(self._user_id)]
        return "/".join(parts)

    def build_dict(self) -> dict:
        return {
            "app_id": self.app_id,
            "scope": self.scope.name,
            "channel": self._channel,
            "extras": self._extra_parts,
            "user_id": self._user_id,
            "wildcard": self._wildcard,
            "topic": self.build() if self._channel else None,
        }

    def __str__(self) -> str:
        return self.build()
    
class SyncCastPayloadBuilder:
    """
    Builds structured notification payloads for SyncCast events.
    Allows setting sender info, core data, metadata, and actions.
    """
    def __init__(self, user_id: str, data_type: str, priority: str = 'normal') -> None:

        self.user_id: str = user_id
        self.type: str = data_type
        self.priority: str = priority
        self.topic: Optional[str] = None
        self.data: Dict[str, Any] = {}
        self.sender_info: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {}
        self.action: Dict[str, str] = {}

    def set_sender_info(self, sender_id: str, sender_name: str, sender_role: Optional[str] = None) -> 'SyncCastPayloadBuilder':
        self.sender_info = {
            "id": sender_id,
            "name": sender_name,
            "role": sender_role or "user"
        }
        return self

    def set_data(self, data: Optional[Dict[str, Any]] = None) -> 'SyncCastPayloadBuilder':
        self.data = data or {}
        return self

    def set_topic(self, topic: str) -> 'SyncCastPayloadBuilder':
        self.topic = topic
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
        payload = {
            "user_id": self.user_id,
            "type": self.type,
            "priority": self.priority,
            "data": self.data,
            "sender": self.sender_info,
            "metadata": self.metadata,
            "action": self.action
        }
        # Include topic at top level
        if self.topic:
            payload["topic"] = self.topic
        return payload