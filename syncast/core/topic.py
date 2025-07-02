# syncast/core/topic.py

from typing import Optional, Dict, Any, Union
from copy import deepcopy
from django.apps import apps
from syncast.models.scope import SyncCastScope

class SyncCastTopicBuilder:
    """
    Builds MQTT topic strings dynamically based on app_id, scope (instance or slug), 
    channel, and optional user or extra parts. Supports wildcards for subscription.
    """
    def __init__(
        self,
        app_id: str,
        scope: Union[str, SyncCastScope],
    ):
        self.app_id = app_id
        self.scope: SyncCastScope = self._resolve_scope(scope)
        self._channel: Optional[str] = None
        self._extra_parts: list[str] = []
        self._user_id: Optional[Union[int, str]] = None
        self._wildcard: bool = False

    def _resolve_scope(self, scope: Union[str, SyncCastScope]) -> SyncCastScope:
        if isinstance(scope, SyncCastScope):
            return scope
        if isinstance(scope, str):
            try:
                return SyncCastScope.objects.prefetch_related("channels").get(slug=scope)
            except SyncCastScope.DoesNotExist:
                raise ValueError(f"Scope with slug '{scope}' does not exist.")
        raise TypeError("Scope must be a SyncCastScope instance or a slug string.")

    def channel(self, channel_name: str) -> 'SyncCastTopicBuilder':
        if not any(c.name == channel_name for c in self.scope.channels.all()):
            valid_channels = [c.name for c in self.scope.channels.all()]
            raise ValueError(
                f"Channel '{channel_name}' not defined for scope '{self.scope.name}'. "
                f"Available: {valid_channels}"
            )
        self._channel = channel_name
        return self

    def extra(self, *parts: Union[str, int]) -> 'SyncCastTopicBuilder':
        self._extra_parts.extend(str(p) for p in parts)
        return self

    def for_user(self, user_id: Union[int, str]) -> 'SyncCastTopicBuilder':
        self._user_id = user_id
        return self

    def wildcard(self) -> 'SyncCastTopicBuilder':
        self._wildcard = True
        return self

    def full_wildcard(self) -> 'SyncCastTopicBuilder':
        self._extra_parts.append("#")
        return self

    def reset(self) -> 'SyncCastTopicBuilder':
        self._channel = None
        self._extra_parts = []
        self._user_id = None
        self._wildcard = False
        return self

    def clone(self) -> 'SyncCastTopicBuilder':
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
