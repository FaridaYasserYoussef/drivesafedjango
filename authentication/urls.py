from django.urls import path

from .views import login
from .views import sign_up


urlpatterns = [
    path("login/", login),
    path("signup/", sign_up)
]