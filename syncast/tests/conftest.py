# syncast/tests/conftest.py

import os
import django
import pytest

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "syncast.tests.settings")

from django.db import connection
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.db import models
# Only setup once
if not django.apps.apps.ready:
    django.setup()

# def create_concrete_model(abstract_model, app_label="syncast_test", model_name=None):
#     name = model_name or f"Test{abstract_model.__name__.replace('Abstract', '')}"

#     # ✅ Return if already registered
#     try:
#         return apps.get_model(app_label, name)
#     except LookupError:
#         pass

#     # ✅ Manually create field dict to patch FKs
#     attrs = {}

#     for field in abstract_model._meta.fields + abstract_model._meta.many_to_many:
#         if isinstance(field, (models.ForeignKey, models.OneToOneField, models.ManyToManyField)):
#             to_model = field.remote_field.model

#             # Skip string references like "auth.User"
#             if isinstance(to_model, str):
#                 continue

#             # Reconstruct field kwargs
#             name, path, args, kwargs = field.deconstruct()

#             # If FK points to an abstract model, replace 'to'
#             if getattr(to_model._meta, "abstract", False):
#                 concrete_target = create_concrete_model(to_model, app_label)
#                 kwargs["to"] = concrete_target

#             # ✅ Reconstruct field cleanly
#             new_field = field.__class__(*args, **kwargs)

#             # ✅ Replace field in model definition
#             attrs[field.name] = new_field

#     # ✅ Inject Meta
#     Meta = type("Meta", (), {
#         "app_label": app_label,
#         "managed": True,
#     })

#     attrs.update({
#         "__module__": __name__,
#         "Meta": Meta,
#         "__test__": False,
#     })

#     # ✅ Define concrete model
#     model = type(name, (abstract_model,), attrs)

#     # ✅ Register
#     apps.register_model(app_label, model)

#     return model


# @pytest.fixture(scope="session")
# def dynamic_room_model(dynamic_scope_model, django_db_setup, django_db_blocker):
#     from django.apps import apps
#     from django.conf import settings
#     from django.db import models
#     from syncast.models.room import AbstractSyncCastRoom

#     with django_db_blocker.unblock():
#         class Meta:
#             app_label = "syncast_test"
#             managed = True

#         model = type("TestRoom", (AbstractSyncCastRoom,), {
#             "__module__": __name__,
#             "Meta": Meta,
#             "__test__": False,
#         })

#         try:
#             return apps.get_model("syncast_test", "TestRoom")
#         except LookupError:
#             apps.register_model("syncast_test", model)
#             return model


# def model_already_registered(app_label, model_name):
#     from django.apps import apps
#     try:
#         apps.get_model(app_label, model_name)
#         return True
#     except LookupError:
#         return False



# # ✅ ONLY import models *after* django.setup()
# from syncast.models.room import AbstractSyncCastRoom
# from syncast.models.tracker import AbstractSyncCastReadTracker
# from syncast.models.presence import AbstractSyncCastUserPresence
# from syncast.models.reaction import AbstractSyncCastReaction

# # Fixtures
# # @pytest.fixture
# # def dynamic_room_model(db):
# #     return create_concrete_model(AbstractSyncCastRoom, model_name="TestRoom")

# @pytest.fixture
# def dynamic_room_model(db):
#     return create_concrete_model(AbstractSyncCastRoom, model_name="TestRoom")

# # @pytest.fixture
# # def setup_dynamic_room_table(dynamic_room_model):
# #     from django.db import connection
# #     with connection.schema_editor() as schema_editor:
# #         schema_editor.create_model(dynamic_room_model)
# #     return dynamic_room_model

# # @pytest.fixture
# # def setup_dynamic_room_table(dynamic_room_model):
# #     from django.db import connection

# #     with connection.cursor() as cursor:
# #         cursor.execute("PRAGMA foreign_keys = OFF;")

# #     with connection.schema_editor() as schema_editor:
# #         schema_editor.create_model(dynamic_room_model)

# #     yield dynamic_room_model

# #     with connection.schema_editor() as schema_editor:
# #         schema_editor.delete_model(dynamic_room_model)

# #     with connection.cursor() as cursor:
# #         cursor.execute("PRAGMA foreign_keys = ON;")

# def ensure_table(model):
#     from django.db import connection
#     with connection.schema_editor() as schema_editor:
#         schema_editor.create_model(model)
        
# @pytest.fixture
# def setup_dynamic_room_table():
#     scope_model = create_concrete_model(AbstractSyncCastScope, model_name="TestSyncCastScope")
#     room_model = create_concrete_model(AbstractSyncCastRoom, model_name="TestSyncCastRoom")

#     for model in [scope_model, room_model]:
#         ensure_table(model)

#     return room_model


# @pytest.fixture
# def dynamic_read_tracker_model(db):
#     return create_concrete_model(AbstractSyncCastReadTracker, model_name="TestReadTracker")

# @pytest.fixture
# def dynamic_presence_model(db):
#     return create_concrete_model(AbstractSyncCastUserPresence, model_name="TestPresence")

# @pytest.fixture
# def dynamic_reaction_model(db):
#     return create_concrete_model(AbstractSyncCastReaction, model_name="TestReaction")

# @pytest.fixture(scope="session")
# def dynamic_scope_model(django_db_setup, django_db_blocker):
#     from syncast.models.scope import AbstractSyncCastScope
#     with django_db_blocker.unblock():
#         return create_concrete_model(AbstractSyncCastScope, model_name="TestScope")

import pytest
from syncast.models.room import AbstractSyncCastRoom
from syncast.tests.model_registry import materialize_model

@pytest.fixture
def dynamic_room_model():
    return materialize_model(AbstractSyncCastRoom, model_name="TestRoom")

@pytest.mark.django_db(transaction=True)
def test_room_creation(dynamic_room_model):
    user_model = dynamic_room_model._meta.get_field("participants").remote_field.model
    scope_model = dynamic_room_model._meta.get_field("scope").related_model

    user = user_model.objects.create(username="testuser")
    scope = scope_model.objects.create(key="test-scope")

    room = dynamic_room_model.objects.create(
        name="Test Room",
        room_type="group",
        scope=scope
    )
    room.participants.add(user)

    assert room.name == "Test Room"
