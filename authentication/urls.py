from django.urls import path

from .views import login
from .views import sign_up
from .views import validate_email
from .views import edit_driver
from .views import getVehicleByDriver
from .views import upload_sensor_data
from .views import upload_video_data



urlpatterns = [
    path("login/", login),
    path("signup/", sign_up),
    path("validate_email/", validate_email),
    path("get_vehicle_by_driver/", getVehicleByDriver),
    path("editProfile/", edit_driver),
    path("upload_sensor_data/", upload_sensor_data),
    path("upload_video_data/", upload_video_data)





]