import os
import uuid
from django.conf import settings

from django.contrib import admin
from polystorage.models.bucket import Bucket

from polystorage.models.bucket_instance import BucketInstance

admin.site.register(Bucket)

@admin.register(BucketInstance)
class BucketInstanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'bucket_type', 'external_provider', 'root_path')
    readonly_fields = ('root_path',)

    def save_model(self, request, obj, form, change):
        if not obj.root_path:
            random_folder = uuid.uuid4().hex[:8]
            base_folder = settings.INSTANCES_MAIN_FOLDER
            obj.root_path = os.path.join(base_folder, random_folder)
        obj.save()