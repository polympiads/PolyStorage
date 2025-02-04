from django.contrib import admin
from polystorage.models.bucket import Bucket

from polystorage.models.bucket_instance import BucketInstance

admin.site.register(Bucket)
admin.site.register(BucketInstance)

# Register your models here.
