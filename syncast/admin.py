from django.contrib import admin

# Register your models here.
from syncast.models.scope import SyncCastScope
from syncast.models.channel import SynCastChannel
from syncast.models.room import SyncCastRoom
from syncast.models.message import SyncCastMessage
from syncast.models.reaction import SynCastMessageReaction
from syncast.models.tracker import SyncCastMessageTracker
from syncast.models.attachment import SyncCastMessageAttachment

@admin.register(SyncCastScope)
class ScopeAdmin(admin.ModelAdmin):
    list_display   = ('id', 'name', 'description')
    search_fields  = ('name',)
    list_filter    = ('name',)
    ordering       = ('name',)

@admin.register(SynCastChannel)
class ChannelAdmin(admin.ModelAdmin):
    list_display   = ('id', 'name', 'scope')
    list_filter    = ('scope__name', 'name')
    search_fields  = ('name', 'scope__name')

@admin.register(SyncCastRoom)
class RoomAdmin(admin.ModelAdmin):
    list_display   = ('id', 'name', 'room_type', 'scope')
    list_filter    = ('room_type', 'scope__name')
    search_fields  = ('name',)
    filter_horizontal = ('participants',)

@admin.register(SyncCastMessage)
class MessageAdmin(admin.ModelAdmin):
    list_display     = ('id', 'room', 'sender', 'created_at', 'is_deleted')
    list_filter      = ('room__scope__name', 'sender', 'is_deleted')
    search_fields    = ('content', 'sender__username')
    date_hierarchy   = 'created_at'

@admin.register(SynCastMessageReaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display   = ('id', 'message', 'user', 'emoji', 'reacted_at')
    list_filter    = ('emoji', 'user')
    search_fields  = ('emoji', 'user__username')
    date_hierarchy = 'reacted_at'

@admin.register(SyncCastMessageTracker)
class StatusAdmin(admin.ModelAdmin):
    list_display   = ('message', 'user', 'is_read', 'delivered_at', 'read_at')
    list_filter    = ('is_read', 'user', 'message__room')
    search_fields  = ('user__username', 'message__content')
    date_hierarchy = 'delivered_at'

@admin.register(SyncCastMessageAttachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display   = ('id', 'message', 'file_type', 'created_at', 'updated_at')
    list_filter    = ('file_type', 'created_at', 'updated_at')
    search_fields  = ('file', 'description')
    date_hierarchy = 'updated_at'