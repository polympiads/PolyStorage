from django.urls import path
from .views import create_bucket_instance, access_bucket_instance

pattern = ([
  path('bucketinst/create/', create_bucket_instance)
], 'bucket', 'bucket')

urlpatterns = [ path('api/v1/', pattern), path('api/v1/bucketinst/<str:name>/', access_bucket_instance) ]