from django.db import models
from django.core.exceptions import ValidationError
import uuid


class Bucket(models.Model):
    objects = models.Manager()  # Default manager
    BUCKET_TYPES = [
        ('STANDARD', 'Standard Storage Bucket'),
        ('EXTERNAL', 'External Provider Bucket')
    ]

    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)

    bucket_type = models.CharField(max_length=20, choices=BUCKET_TYPES, default='STANDARD', editable=False)
    external_provider = models.CharField(max_length=255, null=True, blank=True, editable=False)
    cluster = models.CharField(max_length=255, editable=False)  # Cluster is stored as a string

    write_permission_groups = models.CharField(max_length=1024, blank=True, default='')
    read_permission_groups = models.CharField(max_length=1024, blank=True, default='')
    delete_permission_groups = models.CharField(max_length=1024, blank=True, default='')
    mount_permission_groups = models.CharField(max_length=1024, blank=True, default='')
    observe_permission_groups = models.CharField(max_length=1024, blank=True, default='')

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
        if self.pk:
            orig = Bucket.objects.get(pk=self.pk)
            immutable_fields = ['bucket_type', 'external_provider', 'name', 'created_at', 'cluster']
            for field in immutable_fields:
                if getattr(self, field) != getattr(orig, field):
                    raise ValidationError(f"{field} is immutable and cannot be modified")

        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
