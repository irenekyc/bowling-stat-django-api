# create endpoint
from django.http import JsonResponse
from rest_framework.response import Response
from .models import Team, EventData, EventSummaryData
from .serializers import TeamSerializer, EventDataSerializer, EventSummaryDataSerializer
from rest_framework import status
from rest_framework.decorators import api_view
import numpy as np
from .utlis import *
from .names import *
from .analyize_data import *
import pandas as pd


def team_list(self):
    teams = []
    # get all teams
    teams = Team.objects.all()
    # serialize team data
    serializer = TeamSerializer(teams, many=True)

    # return json
    return JsonResponse({"teams": serializer.data}, safe=False)


@api_view(["GET", "POST"])
def add_team(request, **arg):
    if request.method == "GET":
        return JsonResponse({"error": "API route does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "POST":
        # do something
        data = request.data
        # serializer = TeamSerializer(data=data)
        (addStatus, response) = updateTeamData(data=data)
        if addStatus == SUCCESS:
            return JsonResponse({"team": response.data}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"error": response}, status=status.HTTP_400_BAD_REQUEST)


def team_data(self, **arg):
    teamid_request = arg["teamid"]
    print(teamid_request)
    if teamid_request == None:
        return JsonResponse({"team": {}}, safe=False)
    else:
        try:
            team = Team.objects.get(team_id=teamid_request)
        except Team.DoesNotExist:
            team = None

        if team:
            serializer = TeamSerializer(team, many=False)
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse({"error": "Team does not exist"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET", "POST"])
def add_team_event_data(request, **args):
    if request.method == "GET":
        return JsonResponse({"error": "API route does not exist"}, status=status.HTTP_404_NOT_FOUND)

    teamid_request = request.query_params.get("team")
    eventid_request = request.query_params.get("event")
    if request.method == "POST":
        # do something
        data = request.data
    (status, message) = updateTeamEventData(**data)

    # TODO:
    return JsonResponse({"status": "Work in progress"})


@api_view(["GET", "POST"])
def add_team_event_summary_data(request, **args):
    if request.method == "GET":
        return JsonResponse({"error": "API route does not exist"}, status=status.HTTP_404_NOT_FOUND)

    teamid_request = request.query_params.get("team")
    eventid_request = request.query_params.get("event")

    updateEventSummaryData(data=data, team_id=team_id, event_id=event_id)

    return JsonResponse({"status", "work in progress"})


def team_events_all(self, **args):
    teamid_request = args["teamid"]
    # check if team exist
    try:
        eventdata = EventData.objects.filter(team_id=teamid_request)
        eventdataserializer = EventDataSerializer(eventdata, many=True)

        eventsummarydata = EventSummaryData.objects.filter(team_id=teamid_request)
        eventsummaryserializer = EventSummaryDataSerializer(eventsummarydata, many=True)

        return JsonResponse(
            {
                "data": {"team_id": teamid_request, "event_id": "all", "eventdata": eventdataserializer.data, "eventsummary": eventsummaryserializer.data},
            }
        )
    except EventData.DoesNotExist:
        return JsonResponse({"error": "Empty Data"}, status=status.HTTP_404_NOT_FOUND)


def team_events_single(request, **args):
    teamid_request = args["teamid"]
    eventid_request = args["eventid"]

    try:
        eventdata = EventData.objects.filter(event_id=eventid_request).filter(team_id=teamid_request)
        eventdataserializer = EventDataSerializer(eventdata, many=True)
        eventsummarydata = EventSummaryData.objects.filter(event_id=eventid_request).filter(team_id=teamid_request)
        eventsummaryserializer = EventSummaryDataSerializer(eventsummarydata, many=True)

        return JsonResponse(
            {
                "data": {"team_id": teamid_request, "event_id": eventid_request, "eventdata": eventdataserializer.data, "eventsummary": eventsummaryserializer.data},
            }
        )
    except EventData.DoesNotExist:
        return JsonResponse({"error": "Empty Data"})


@api_view(["GET", "POST"])
def upload_event_csv(request, **args):
    if request.method == "GET":
        return JsonResponse({"error": "API route does not exist"}, status=status.HTTP_404_NOT_FOUND)

    meta_data = request.data
    meta_data["file"] = request.FILES["file"]
    team_name = meta_data["team_name"]
    (analyized_records, summary_records, team_id, event_id) = analyize_data(**meta_data)
    (summaryUpdateStatus, message) = updateEventSummaryData(data=summary_records, team_id=team_id, event_id=event_id)
    (teamEventDataUpdateStatus, team_event_data) = updateTeamEventData(data=analyized_records, team_id=team_id, event_id=event_id)
    bowlers = []
    for summary_entry in summary_records:
        bowlers.append(summary_entry["bowler"])

    bowlersStr = ",".join(bowlers)
    events = event_id
    team = {"team_id": team_id, "team_name": team_name, "bowlers": bowlersStr, "events": events}
    (teamUpdateStatus, team_data) = updateTeamData(data=team)
    if summaryUpdateStatus == SUCCESS and teamEventDataUpdateStatus == SUCCESS and teamUpdateStatus == SUCCESS:
        return JsonResponse({"status": "updated", "team_id": team_id, "event_id": event_id})

    return JsonResponse({"error": "something wrong"})
