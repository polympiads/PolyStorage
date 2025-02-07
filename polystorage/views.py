import uuid
import os

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
        return JsonResponse({
                "error": "Invalid request method",
                "reasons": ["Expected POST"]
        }, status=400)

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
        payload = json.loads(payload)
    except JWTError:
        return HttpResponseBadRequest("Invalid signature")

    required_fields = ["name", "bucket_type", "external_provider", "mount_permissions"]
    missing_fields = [field for field in required_fields if field not in payload]

    if missing_fields:
        return HttpResponseBadRequest(f"Missing required fields: {', '.join(missing_fields)}")

    if BucketInstance.objects.contains(payload["name"]):
        return HttpResponseBadRequest(f"Bucket instance already exists: {payload['name']}")

    # Generate root_path on the cluster
    random_folder = uuid.uuid4().hex[:8]
    base_folder = settings.INSTANCES_MAIN_FOLDER
    generated_root_path = os.path.join(base_folder, random_folder)

    bucket_instance = BucketInstance.objects.create(
        name=payload["name"],
        root_path=generated_root_path, # Use the generated root path
        bucket_type=payload["bucket_type"],
        external_provider=payload["external_provider"],
        mount_permissions=payload["mount_permissions"]
    )

    return JsonResponse({
        "message": "Bucket instance created successfully",
        "id": bucket_instance.id,
        "root_path": generated_root_path # Include in JSON response
    })