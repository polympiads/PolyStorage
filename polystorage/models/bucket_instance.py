from django.db import models
from django.core.exceptions import ValidationError
from polystorage.constants import BUCKET_TYPES

class BucketInstance(models.Model):
    objects = models.Manager()  # Default manager

    name = models.CharField(max_length=255)
    root_path = models.CharField(max_length=255)
    bucket_type = models.CharField(max_length=20, choices=BUCKET_TYPES, default='STANDARD')
    external_provider = models.CharField(max_length=255, null=True, blank=True)
    mount_permissions = models.CharField(max_length=1024, blank=True, default='')

    class Meta:
        db_table = 'storage_bucket_instance'
        ordering = ['name']

    def clean(self):
        if self.bucket_type == 'EXTERNAL':
            if not self.external_provider:
                raise ValidationError("External buckets must specify a provider")

    def save(self, *args, **kwargs):
        if self.pk:
            orig = BucketInstance.objects.get(pk=self.pk)
            immutable_fields = ['name', 'root_path', 'bucket_type', 'external_provider', 'mount_permissions']
            for field in immutable_fields:
                if getattr(self, field) != getattr(orig, field):
                    raise ValidationError(f"{field} is immutable and cannot be modified")

        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"