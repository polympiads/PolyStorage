import requests
from django.test import TestCase, Client, override_settings
from django.conf import settings
from django.utils.timezone import override


class CreateBucketInstanceTest(TestCase):
    @override_settings(ROOT_URLCONF='polystorage.urls')
    def test_create_bukect_instance (self):
        client = Client()
        url = ('http://localhost:8000/api/v1/bucketinst/create/')
        headers = {'Content-Type': 'application/json'}

        data = {
            "name": "TestBucket",
            "root_path": "/mnt/data",
            "bucket_type": "STANDARD",
            "external_provider": "",
            "mount_permissions": ""
        }

        response = client.post(url, json=data, headers=headers) # Sends JSON in body

        print("Status Code:", response.status_code)