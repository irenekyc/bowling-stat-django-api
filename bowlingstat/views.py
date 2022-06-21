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


def team_events_all(self, **args):
    teamid_request = args["teamid"]
    # check if team exist
    try:
        team = EventData.objects.filter(team_id=teamid_request)
    except EventData.DoesNotExist:
        team = None

    if team:
        # return team event data
        serializer = EventDataSerializer(team, many=True)
        return JsonResponse({"data": serializer.data})
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


def team_events_summary_all(request, **args):
    team_id = args["teamid"]
    # return JsonResponse({"status": "Work in progress"})
    try:
        team = EventSummaryData.objects.filter(team_id=team_id)
    except EventSummaryData.DoesNotExist:
        team = None

    if team:
        # return team event data
        serializer = EventSummaryDataSerializer(team, many=True)
        return JsonResponse({"data": serializer.data})
    else:
        return JsonResponse({"error": "Team does not exist"}, status=status.HTTP_404_NOT_FOUND)


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
        return JsonResponse({"status": "updated"})

    return JsonResponse({"error": "something wrong"})
