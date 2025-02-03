import requests

url = ('http://localhost:8000/api/v1/bucketinst/create/')
headers = {'Content-Type': 'application/json'}

data = {
    "name": "TestBucket",
    "root_path": "/mnt/data",
    "bucket_type": "STANDARD",
    "external_provider": "",
    "mount_permissions": ""
}

response = requests.post(url, json=data, headers=headers) # Sends JSON in body

print("Status Code:", response.status_code)
print("Raw Response Text:", response.text) # Print the server response

try:
    print("JSON Response:", response.json()) # Handle JSON response safely
except requests.exceptions.JSONDecodeError:
    print("Non-JSON response:", response.text)