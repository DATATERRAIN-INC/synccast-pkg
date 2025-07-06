# Default package imports
import pytest

# Django imports
from django.db import models
from django.db import models, connection

# SyncCast abstract model
from synccast.models.scope import AbstractSyncCastScope
from synccast.models.channel import AbstractSyncCastChannel

# syncCast paylod
from synccast.core.topic import SyncCastTopicBuilder

# synccast custom exceptions
from synccast.exceptions import SyncCastTopicError

# syncCast client singelton instance
from synccast import synccast

# syncCast test
from synccast.tests.utils.dynamic_models import create_test_model

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
        SyncCastTopicBuilder(synccast.app_id or 'XJWKLMNOPQWZURW', scope)
        .channel("message")
        .for_user(42)
        .extra("room", 5)
        .build()
    )
    
    assert topic == f"XJWKLMNOPQWZURW/Chat/message/room/5/user/42"
