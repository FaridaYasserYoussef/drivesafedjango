from django.urls import path

from .views import save_trip

urlpatterns = [
    path("save_trip/", save_trip),
 
]