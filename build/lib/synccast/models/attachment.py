# synccast/models/attachment.py

# Django imports
from django.db import models

# SyncCast abstract model
from synccast.models.base import AbstractSyncCastBaseModel

# SyncCast models mixins
from synccast.models.mixins import EnforcedFKTargetsMixin
class AbstractSyncCastAttachment(EnforcedFKTargetsMixin, AbstractSyncCastBaseModel):
    """
    Represents an attachment to a message, e.g., images, files.
    Tied to a specific message.
    """
    class SyncCastAttachmentType(models.TextChoices):
        # Images
        JPEG = "jpeg", "JPEG Image"
        JPG = "jpg", "JPG Image"
        PNG = "png", "PNG Image"
        GIF = "gif", "GIF Image"
        WEBP = "webp", "WebP Image"

        # Documents
        PDF = "pdf", "PDF Document"
        TXT = "txt", "Text File"
        DOC = "doc", "Word Document"
        DOCX = "docx", "Word Document (.docx)"
        XLS = "xls", "Excel Spreadsheet"
        XLSX = "xlsx", "Excel Spreadsheet (.xlsx)"
        PPT = "ppt", "PowerPoint Presentation"
        PPTX = "pptx", "PowerPoint (.pptx)"

        # Audio
        MP3 = "mp3", "MP3 Audio"
        WAV = "wav", "WAV Audio"
        OGG = "ogg", "OGG Audio"

        # Video
        MP4 = "mp4", "MP4 Video"
        MOV = "mov", "MOV Video"
        AVI = "avi", "AVI Video"
        WEBM = "webm", "WebM Video"
        MKV = "mkv", "MKV Video"

        # Archives
        ZIP = "zip", "ZIP Archive"
        RAR = "rar", "RAR Archive"
        TAR = "tar", "TAR Archive"
        GZ = "gz", "GZip Archive"

        # Fallback
        OTHER = "other", "Other"

    REQUIRED_FK_TARGETS = [
        "synccast.models.message.AbstractSyncCastMessage"
    ]

    file = models.FileField(
        upload_to='message_attachments/',
        help_text="The attached file."
    )

    file_type = models.CharField(
        max_length=10,
        choices=SyncCastAttachmentType.choices,
        default=SyncCastAttachmentType.OTHER,
        help_text="Type of the attachment, e.g., image, file, video."
    )

    description = models.TextField(
        blank=True,
        help_text="Optional description of the attachment."
    )

    class Meta:
        abstract = True

     
