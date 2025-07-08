# Default package imports
from typing import Optional, Dict, Any, Union
from copy import deepcopy

# Django imports
from django.apps import apps

# SyncCast custom exceptions
from synccast.exceptions.types import SyncCastTopicError
class SyncCastTopicBuilder:

    """
    Builds MQTT topic strings dynamically based on app_id, scope (instance or slug), 
    channel, and optional user or extra parts. Supports wildcards for subscription.
    """

    def __init__(
        self,
        app_id: str,
        scope: Union[str, object],  # Accepts either a slug or model instance
    ):
        self.app_id = app_id or "default-app"  # fallback for dev
        self.scope = self._resolve_scope(scope)
        self._channel: Optional[str] = None
        self._extra_parts: list[str] = []
        self._user_id: Optional[Union[int, str]] = None
        self._wildcard: bool = False

    @staticmethod
    def _get_concrete_scope_model():
        """
        Dynamically find the concrete model subclassing AbstractSyncCastScope.
        """
        from synccast.models.scope import AbstractSyncCastScope

        for model in apps.get_models():
            if issubclass(model, AbstractSyncCastScope) and not model._meta.abstract:
                return model

        raise LookupError("No concrete model found inheriting from AbstractSyncCastScope.")
    
    
    @staticmethod
    def get_channel_related_manager(scope_instance):
        from synccast.models.channel import AbstractSyncCastChannel
        for rel in scope_instance._meta.related_objects:
            if issubclass(rel.related_model, AbstractSyncCastChannel):
                return getattr(scope_instance, rel.get_accessor_name())  # i.e., scope.channels
        raise LookupError("No SyncCastChannel relation found.")

    def _resolve_scope(self, scope: Union[str, object]):
        from synccast.models.scope import AbstractSyncCastScope

        if isinstance(scope, AbstractSyncCastScope):  # safest check
            try:
                self.get_channel_related_manager(scope)
                return scope
            except LookupError:
                pass

        if isinstance(scope, str):
            try:
                ScopeModel = self._get_concrete_scope_model()

                # Fetch one object (no prefetch here — since related name is dynamic)
                instance = ScopeModel.objects.get(name=scope)

                # Trigger channel manager to cache related objects if needed (lazy eval is fine)
                self.get_channel_related_manager(instance)

                return instance
            except Exception as e:
                raise SyncCastTopicError(
                    message=f"Scope with slug '{scope}' not found or failed to load.",
                    extra={"slug": scope, "error": str(e)}
                ) from e

        raise SyncCastTopicError(
            message="Invalid scope type. Must be a slug or model instance.",
            extra={"provided_type": type(scope).__name__}
        )

    def channel(self, channel_name: str) -> 'SyncCastTopicBuilder':
        try:
            channel_manager = self.get_channel_related_manager(self.scope)
        except Exception as e:
            raise SyncCastTopicError(
                message=f"Scope object does not have a valid channel relation.",
                extra={"scope": str(self.scope), "error": str(e)}
            ) from e

        if not any(c.name == channel_name for c in channel_manager.all()):
            valid_channels = [c.name for c in channel_manager.all()]
            raise SyncCastTopicError(
                message=f"Channel '{channel_name}' not defined for scope '{self.scope.name}'.",
                extra={"channel": channel_name, "valid_channels": valid_channels}
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
            raise SyncCastTopicError(
                message="Channel must be set before building topic",
                extra={"scope": self.scope.name, "app_id": self.app_id}
            )

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
