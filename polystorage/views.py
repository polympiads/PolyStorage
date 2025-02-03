from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest

from .models.bucket_instance import BucketInstance


def create_bucket_instance(request, *args, **kwargs):
    assert request.method == 'POST'
    assert "name" in request.POST
    assert "root_path" in request.POST
    assert "bucket_type" in request.POST
    assert "external_provider" in request.POST
    assert "mount_permissions" in request.POST

    bucket_instance = BucketInstance.objects.create()
    bucket_instance.name = request.POST["name"]
    bucket_instance.root_path = request.POST["root_path"]
    bucket_instance.bucket_type = request.POST["bucket_type"]
    bucket_instance.external_provider = request.POST["external_provider"]
    bucket_instance.mount_permissions = request.POST["mount_permissions"]
    bucket_instance.save()