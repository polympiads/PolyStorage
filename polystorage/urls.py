from django.urls import path, include
from .views import create_bucket_instance, access_bucket_instance

bucket_patterns = [
  path('create/', create_bucket_instance, name='create_bucket_instance'),
  path('<str:name>/', access_bucket_instance, name='access_bucket_instance'),
]

urlpatterns = [
  path('api/v1/bucketinst/', include((bucket_patterns, 'bucket')))
]