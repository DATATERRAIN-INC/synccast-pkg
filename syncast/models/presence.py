# syncast/models/presence.py

# Django imports
from django.db import models
from django.conf import settings
from django.utils import timezone

class SyncCastUserPresence(models.Model):
    """Tracks real-time presence and activity status of users."""

    class PresenceStatus(models.TextChoices):
        ONLINE = "online", "Online"
        OFFLINE = "offline", "Offline"
        AWAY = "away", "Away"
        IDLE = "idle", "Idle"
        TYPING = "typing", "Typing"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="presences",
        help_text="The user whose presence is being tracked. Links to the AUTH_USER_MODEL."
    )

    status = models.CharField(
        max_length=16,
        choices=PresenceStatus.choices,
        default="offline",
        help_text="Current presence status of the user. Choices: online, offline, away, idle, typing."
    )

    last_seen_at = models.DateTimeField(
        default=timezone.now,
        help_text="Timestamp when the user was last seen active (updated manually by backend)."
    )

    last_updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of the most recent status update (auto-set on save)."
    )

    screen = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text="Frontend screen or route the user is currently on. Example: 'chat/room/123' or 'dashboard'."
    )

    device_info = models.JSONField(
        blank=True,
        null=True,
        help_text="Metadata about the user's device or client. May include browser, OS, platform, app version, etc."
    )

    class Meta:
        abstract = True
