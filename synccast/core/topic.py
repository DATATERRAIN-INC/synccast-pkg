from typing import Optional, Union, List, Dict
from copy import deepcopy
from django.apps import apps
from synccast.exceptions.types import SyncCastTopicError


class SyncCastTopicBuilder:
    """
    Builds MQTT topic strings in a fixed format:
    app_id/scope/(extra...)/user/{id or +}/channel[/#]
    Enforces consistency, channel validation, and user presence.
    """

    def __init__(self, app_id: str, scope: Union[str, object]):
        self.app_id = app_id or "default-app"
        self.scope = self._resolve_scope(scope)

        self._channel: Optional[str] = None
        self._extra_parts: List[str] = []
        self._user_id: Optional[Union[int, str]] = None
        self._wildcard: bool = False
        self._full_wildcard: bool = False

    @staticmethod
    def _get_concrete_scope_model():
        from synccast.models.scope import AbstractSyncCastScope
        for model in apps.get_models():
            if issubclass(model, AbstractSyncCastScope) and not model._meta.abstract:
                return model
        raise LookupError("No concrete model found inheriting from AbstractSyncCastScope.")

    @staticmethod
    def get_channel_related_manager(scope_instance):
        from synccast.models.channel import AbstractSyncCastChannel
        for field in scope_instance._meta.get_fields():
            if (
                field.is_relation and field.auto_created and not field.concrete
                and hasattr(field, "related_model")
                and issubclass(field.related_model, AbstractSyncCastChannel)
            ):
                return getattr(scope_instance, field.get_accessor_name())
        raise LookupError("No SyncCastChannel reverse relation found on scope model.")

    def _resolve_scope(self, scope: Union[str, object]):
        from synccast.models.scope import AbstractSyncCastScope

        if isinstance(scope, AbstractSyncCastScope) and not scope._meta.abstract:
            try:
                self.get_channel_related_manager(scope)
                return scope
            except LookupError:
                pass

        if isinstance(scope, str):
            try:
                ScopeModel = self._get_concrete_scope_model()
                instance = ScopeModel.objects.get(name=scope)
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

    def channel(self, channel_name: str, validate: bool = True) -> 'SyncCastTopicBuilder':
        if validate:
            try:
                channel_manager = self.get_channel_related_manager(self.scope)
            except Exception as e:
                raise SyncCastTopicError(
                    message="Scope object does not have a valid channel relation.",
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
        self._user_id = str(user_id)
        return self

    def wildcard(self) -> 'SyncCastTopicBuilder':
        self._wildcard = True
        return self

    def full_wildcard(self) -> 'SyncCastTopicBuilder':
        self._full_wildcard = True
        return self

    def reset(self) -> 'SyncCastTopicBuilder':
        self._channel = None
        self._extra_parts = []
        self._user_id = None
        self._wildcard = False
        self._full_wildcard = False
        return self

    def clone(self) -> 'SyncCastTopicBuilder':
        return deepcopy(self)

    def is_valid(self) -> bool:
        return self._channel is not None and (self._user_id is not None or self._wildcard)

    def build(self) -> str:
        if not self._channel:
            raise SyncCastTopicError(
                message="Channel must be set before building topic",
                extra={"scope": getattr(self.scope, 'name', '<unknown>'), "app_id": self.app_id}
            )

        if self._user_id is None and not self._wildcard:
            raise SyncCastTopicError(
                message="User ID must be specified using .for_user(...) or wildcard() before building topic.",
                extra={"scope": getattr(self.scope, 'name', '<unknown>'), "channel": self._channel}
            )

        parts = [self.app_id, self.scope.name]
        parts.extend(self._extra_parts)
        parts.extend(["user", "+" if self._wildcard else self._user_id])
        parts.append(self._channel)

        if self._full_wildcard:
            parts.append("#")

        return "/".join(parts)

    def build_dict(self) -> Dict[str, Union[str, List[str], bool, None]]:
        return {
            "app_id": self.app_id,
            "scope": getattr(self.scope, "name", None),
            "channel": self._channel,
            "extras": self._extra_parts,
            "user_id": self._user_id,
            "wildcard": self._wildcard,
            "topic": self.build() if self.is_valid() else None,
        }

    def __str__(self) -> str:
        return self.build()
