import pytest
from syncast.core.payload import SyncCastPayloadBuilder
from syncast.core.enums import SyncCastEventType, SyncCastPriorityLevel, SyncCastQosLevel
from syncast.exceptions.core import SyncCastPayloadError

from syncast.models.scope import AbstractSyncCastScope

from unittest.mock import patch

class DummyScope:
    slug = "mocked-scope"

 
def test_minimal_payload_build():
    builder = SyncCastPayloadBuilder(user=123)
    builder.set_topic("test/topic")

    payload = builder.build()

    assert payload["user_id"] == "123"
    assert payload["type"] == SyncCastEventType.PUSH_ALERT.value
    assert payload["priority"] == SyncCastPriorityLevel.MEDIUM.value
    assert payload["qos"] == SyncCastQosLevel.DELIVER_AT_LEAST_ONCE.value
    assert payload["topic"] == "test/topic"

def test_full_payload_build():
    builder = (
        SyncCastPayloadBuilder(user="u001", type=SyncCastEventType.CHAT_MESSAGE)
        .set_topic("chat/room/42")
        .set_scope("chat")
        .set_data({"text": "Hello"})
        .set_sender_info("42", "Alice", "admin")
        .set_metadata("iOS", "iPhone 14", "New York")
        .set_action("open_chat", "/chat/42")
    )

    payload = builder.build()

    assert payload["user_id"] == "u001"
    assert payload["type"] == SyncCastEventType.CHAT_MESSAGE.value
    assert payload["scope"] == "chat"
    assert payload["data"] == {"text": "Hello"}
    assert payload["sender"]["name"] == "Alice"
    assert payload["metadata"]["device"] == "iPhone 14"
    assert payload["action"]["url"] == "/chat/42"


def test_invalid_scope_raises():
    builder = SyncCastPayloadBuilder()
    with pytest.raises(SyncCastPayloadError) as exc:
        builder.set_scope(1234)
    assert "Scope must be a string or SyncCastScope instance" in str(exc.value)

def test_invalid_topic_raises():
    builder = SyncCastPayloadBuilder()
    with pytest.raises(SyncCastPayloadError) as exc:
        builder.set_topic(None)
    assert "Invalid topic format" in str(exc.value)

def test_missing_topic_on_build_raises():
    builder = SyncCastPayloadBuilder(user=1)
    with pytest.raises(SyncCastPayloadError) as exc:
        builder.build()
    assert "Payload missing required 'topic'" in str(exc.value)

def test_str_method_outputs_payload():
    builder = SyncCastPayloadBuilder(user="123").set_topic("topic/test")
    payload_str = str(builder)
    assert "'user_id': '123'" in payload_str  # match single-quote format
    assert "'topic': 'topic/test'" in payload_str



 