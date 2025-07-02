# tests/test_topic_builder.py

# ⚠️ Configure Django BEFORE importing any models
import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        SECRET_KEY="test",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "syncast",  # Your app name
        ],
        AUTH_USER_MODEL="auth.User",
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        USE_TZ=True,
    )
    django.setup()

# ✅ Now it's safe to import models and other Django modules
from syncast.core.topic import SyncCastTopicBuilder

# Mock implementations for testing
class MockChannel:
    def __init__(self, name: str):
        self.name = name

class MockScope:
    def __init__(self, name: str, channel_names: list[str]):
        self.name = name
        self._channels = [MockChannel(n) for n in channel_names]

    @property
    def channels(self):
        class ChannelSet:
            def __init__(self, channels):
                self._channels = channels

            def all(self):
                return self._channels

        return ChannelSet(self._channels)

# Test function
def test_topic_builder():
    app_id = "test_app"
    scope = MockScope(name="chat", channel_names=["message", "typing", "presence"])

    builder = (
        SyncCastTopicBuilder(app_id=app_id, scope=scope)
        .channel("typing")
        .extra("room42")
        .for_user("99")
    )

    topic = builder.build()
    expected = "test_app/chat/typing/room42/user/99"
    
    assert topic == expected, f"❌ Unexpected topic: {topic} (expected {expected})"
    print("✅ Topic built successfully:", topic)

# Run it
if __name__ == "__main__":
    test_topic_builder()
