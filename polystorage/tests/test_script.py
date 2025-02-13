import requests
from django.test import TestCase, Client, override_settings
from django.conf import settings
from django.utils.timezone import override
from jose import jws
import json

from polystorage.models.bucket_instance import BucketInstance


class CreateBucketInstanceTest(TestCase):
    @override_settings(ROOT_URLCONF='polystorage.urls')
    def setUp(self):
        self.client = Client()
        self.url = settings.API_URL + '/api/v1/bucketinst/create/'
        self.headers = {'Content-Type': 'application/json'}
        self.private_key = settings.STORAGE_ROOT_PRIVATE_KEY

    def generate_signed_data(self, payload):
        return jws.sign(payload, self.private_key, algorithm='RS256')

    def test_create_bucket_instance_success(self):
        payload = {
            "name": "TestBucket",
            "bucket_type": "STANDARD",
            "external_provider": "",
            "mount_permissions": ""
        }
        signed_data = self.generate_signed_data(payload)
        response = self.client.post(self.url, json.dumps({"signed_data": signed_data}), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Bucket instance created successfully')
        self.assertIn('id', response_data)
        self.assertIn('root_path', response_data)

    def test_invalid_request_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid request method')

    def test_missing_signed_data(self):
        response = self.client.post(self.url, json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Missing signed_data')

    def test_invalid_signature(self):
        invalid_signed_data = 'invalid.signature.data'
        response = self.client.post(self.url, json.dumps({"signed_data": invalid_signed_data}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid signature')

    def test_missing_required_fields(self):
        incomplete_payload = {
            "name": "TestBucket"
        }
        signed_data = self.generate_signed_data(incomplete_payload)
        response = self.client.post(self.url, json.dumps({"signed_data": signed_data}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required fields', response.content.decode())