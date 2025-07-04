import pytest
from django.db import models
from syncast.models.scope import AbstractSyncCastScope
from syncast.models.channel import AbstractSyncCastChannel
from syncast.core.topic import SyncCastTopicBuilder
from syncast.exceptions import SyncCastTopicError
from django.db import models, connection
from syncast.tests.utils.dynamic_models import create_test_model

@pytest.mark.django_db(transaction=True)  # <-- VERY IMPORTANT
def test_topic_builder_with_dynamic_models():
    # ✅ Disable foreign key checks at the connection level
    if connection.vendor == "sqlite":
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA foreign_keys = OFF;")

    # ✅ Don't use a fixture here — create models inside test
    Scope = create_test_model("Scope", AbstractSyncCastScope)

    Channel = create_test_model("Channel", AbstractSyncCastChannel, {
        "scope": models.ForeignKey(Scope, related_name="channels", on_delete=models.CASCADE)
    })

    scope = Scope.objects.create(name="Chat")
    Channel.objects.create(name="message", scope=scope)

    topic = (
        SyncCastTopicBuilder(scope)
        .channel("message")
        .for_user(42)
        .extra("room", 5)
        .build()
    )
    print(type(topic), topic)

    assert topic == f"default-app/Chat/message/room/5/user/42"
