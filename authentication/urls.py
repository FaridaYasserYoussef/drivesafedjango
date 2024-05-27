from django.urls import path

from .views import login
from .views import sign_up
from .views import validate_email


urlpatterns = [
    path("login/", login),
    path("signup/", sign_up),
    path("validate_email/", validate_email),
    path("get_vehicle_by_driver/", validate_email)


]