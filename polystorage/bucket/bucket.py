from django.db import models
from django.core.exceptions import ValidationError
import uuid


class Bucket(models.Model):
    BUCKET_TYPES = [
        ('STANDARD', 'Standard Storage Bucket'),
        ('EXTERNAL', 'External Provider Bucket')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)

    bucket_type = models.CharField(max_length=20, choices=BUCKET_TYPES, default='STANDARD')
    external_provider = models.CharField(max_length=255, null=True, blank=True)
    root_path = models.CharField(max_length=1024, default='/')

    mount_enabled = models.BooleanField(default=False)
    observe_enabled = models.BooleanField(default=False)

    class Meta:
        db_table = 'storage_bucket'
        ordering = ['name', 'created_at']

    def clean(self):
        if self.mount_enabled and self.observe_enabled:
            raise ValidationError("A bucket cannot implement both MOUNT and OBSERVE operations")

        if self.bucket_type == 'EXTERNAL':
            if not self.external_provider:
                raise ValidationError("External buckets must specify a provider")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.id})"
