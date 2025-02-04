from django.shortcuts import render

from .models.bucket_instance import BucketInstance
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from jose import jws, JWTError
import json
from django.conf import settings

@csrf_exempt
def create_bucket_instance(request, *args, **kwargs):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method. Expected POST")

    try:
        data = json.loads(request.body.decode("utf-8"))
        signed_data = data.get("signed_data")
        if not signed_data:
            return HttpResponseBadRequest("Missing signed_data")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON format")

    try:
        public_key = settings.STORAGE_ROOT_PUBLIC_KEY
        payload = jws.verify(signed_data, public_key, algorithms=["RS256"])
    except JWTError:
        return HttpResponseBadRequest("Invalid signature")

    required_fields = ["name", "root_path", "bucket_type", "external_provider", "mount_permissions"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return HttpResponseBadRequest(f"Missing required fields: {', '.join(missing_fields)}")

    bucket_instance = BucketInstance.objects.create(
        name=data["name"],
        root_path=data["root_path"],
        bucket_type=data["bucket_type"],
        external_provider=data["external_provider"],
        mount_permissions=data["mount_permissions"]
    )

    return JsonResponse({"message": "Bucket instance created successfully", "id": bucket_instance.id})