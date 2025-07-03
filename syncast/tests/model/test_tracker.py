def test_tracker_creation(dynamic_read_tracker_model):
    tracker = dynamic_read_tracker_model.objects.create(user_id=42)
    assert tracker.user_id == 42
