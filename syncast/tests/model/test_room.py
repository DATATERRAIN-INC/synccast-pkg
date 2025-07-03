import pytest
from django.contrib.auth import get_user_model

@pytest.mark.django_db(transaction=True)
def test_room_creation(dynamic_room_model):
    room_model = dynamic_room_model
    user = get_user_model().objects.create_user(username="testuser", password="testpass")

    # Create scope
    scope_model = room_model._meta.get_field("scope").related_model
    scope = scope_model.objects.create(name="room-123")

    # Create room and add participant
    room = room_model.objects.create(name="Test Room", room_type="group", scope=scope)
    room.participants.add(user)

    assert room.participants.count() == 1      # ✅ YES