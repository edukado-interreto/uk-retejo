from django.urls import path
from .views import get_registration, loaddata

urlpatterns = [
    path("loaddata", loaddata),
    path("getRegistration", get_registration),
]
