from django.urls import path
from . import views

urlpatterns = [
    path('stream/', views.sse_stream, name='sse_stream'),
]
