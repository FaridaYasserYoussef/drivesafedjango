from django.db import models
from segmentor.models import Segment
# Create your models here.

class SegmentClass(models.Model):
    segment_id = models.ForeignKey(Segment, on_delete=models.CASCADE)
    segment_class =  models.CharField(max_length=500)
    