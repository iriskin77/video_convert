import uuid
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.


class VideoFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to="video_files")
    width = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(20)])
    height = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(20)])
    is_processing = models.BooleanField(default=None, null=True, blank=True)
    processing_success = models.BooleanField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename
