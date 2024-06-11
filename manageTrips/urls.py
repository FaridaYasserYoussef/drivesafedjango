from django.urls import path

from .views import save_trip, getAllDriverTrips, sse_stream, get_trip_events

urlpatterns = [
    path("save_trip/", save_trip),
    path("get_driver_trips/", getAllDriverTrips),
    path("sse-stream/<int:driver_id>", sse_stream),
    path("get_trip_events/", get_trip_events)

 
]