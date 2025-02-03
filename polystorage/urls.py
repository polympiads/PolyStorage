from django.urls import path
from .views import create_bucket_instance

pattern = ([
  path('bucketinst/create/', create_bucket_instance)
], 'bucket', 'bucket')

urlpatterns = [ path('api/v1/', pattern) ]