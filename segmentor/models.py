from django.db import models
from manageTrips.models import Trip
from authentication.models import Driver
# Create your models here.


class SegmentType(models.Model):
    type = models.CharField(max_length=500)


class Segment(models.Model):
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE)
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    segment_path = models.CharField(max_length=500)
    Segment_type = models.ForeignKey(SegmentType, on_delete=models.CASCADE)

