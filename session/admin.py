from django.contrib import admin
from .models import MultiplyerData, RespiratoryGraphData, SustainedAttentionData

admin.site.register(MultiplyerData)
admin.site.register(RespiratoryGraphData)
admin.site.register(SustainedAttentionData)