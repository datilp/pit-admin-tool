from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path("testapi/", views.TestAPIView.as_view(), name='testapi'),
    path("testapi2/", views.TestAPIView2.as_view(), name='testapi2'),
]