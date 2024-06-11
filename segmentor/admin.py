from django.contrib import admin
from .models import SegmentType
# Register your models here.

@admin.register(SegmentType)
class SegmentTypeAdmin(admin.ModelAdmin):
    pass

