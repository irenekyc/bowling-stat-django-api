# from python object to json (api friendly)

from .models import Team, EventData, EventSummaryData
from rest_framework import serializers


class TeamSerializer(serializers.ModelSerializer):
    # describe the model
    class Meta:
        model = Team
        fields = "__all__"


class EventDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventData
        fields = "__all__"


class EventSummaryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventSummaryData
        fields = "__all__"
