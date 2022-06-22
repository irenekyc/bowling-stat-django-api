from django.contrib import admin
from .models import Team, EventData, EventSummaryData

admin.site.register(Team)
admin.site.register(EventData)
admin.site.register(EventSummaryData)
