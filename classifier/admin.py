from django.contrib import admin
from .models import SegmentClass
# Register your models here.


@admin.register(SegmentClass)
class SegmentClassAdmin(admin.ModelAdmin):
    pass