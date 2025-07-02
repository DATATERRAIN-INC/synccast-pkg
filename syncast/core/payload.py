# Package imports
from typing import Optional, Dict, Any, Union, Self
from copy import deepcopy

# Module imports
from syncast.models import SyncCastScope
from syncast.core.enums import SyncCastEventType, SyncCastPriorityLevel, SyncCastQosLevel

class SyncCastPayloadBuilder:
    """
    Builds structured notification payloads for SyncCast events.
    Allows setting sender info, core data, metadata, and actions.
    """
    def __init__(
            self, 
            user: int, 
            type: SyncCastEventType = SyncCastEventType.PUSH_ALERT, 
            priority: SyncCastPriorityLevel = SyncCastPriorityLevel.MEDIUM,
            qos: SyncCastQosLevel = SyncCastQosLevel.DELIVER_AT_LEAST_ONCE
        ) -> None:

        self.user: str = user
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
            "role": sender_role or "user"
        }
        return self

    def set_data(self, data: Optional[Dict[str, Any]] = None) -> 'SyncCastPayloadBuilder':
        self.data = data or {}
        return self
    
    def set_topic(self, topic: str) -> 'SyncCastPayloadBuilder':
        self.topic = topic
        return self
    
    def set_scope(self, scope: Union[SyncCastScope, str]) -> 'SyncCastPayloadBuilder':
        """
        Sets the scope from a model instance or a raw string slug.
        """
        if isinstance(scope, SyncCastScope):
            self.scope = scope.slug  # or `.name` if that's your field
        elif isinstance(scope, str):
            self.scope = scope
        else:
            raise ValueError("Invalid scope. Must be a SyncCastScope instance or a slug string.")
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
         
        return payload