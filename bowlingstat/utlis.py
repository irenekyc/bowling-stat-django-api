from .models import Team, EventSummaryData, EventData
from django.http import JsonResponse
from .serializers import TeamSerializer, EventDataSerializer, EventSummaryDataSerializer
from rest_framework import status
import numpy as np
from .names import *


def checkIfTeamExistInTeamData(team_id):
    try:
        team = Team.objects.get(team_id=team_id)
        return team
    except Team.DoesNotExist:
        return None


def updateExistingTeamData(team, updated_bowlers_str, updated_event_ids_str):
    print("team data exist")
    # get bowlers
    current_bowler_list = team.bowlers.split(",")
    current_bowler_list = [bowler.strip() for bowler in current_bowler_list]
    request_bowlers = updated_bowlers_str.split(",")
    request_bowlers = [bowler.strip() for bowler in request_bowlers]
    appended_bowler_list = current_bowler_list + request_bowlers
    appended_bowler_list = np.unique(appended_bowler_list)

    # get events
    current_events_list = team.events.split(",")
    current_events_list = [events.strip() for events in current_events_list]
    request_events = updated_event_ids_str.split(",")
    request_events = [event.strip() for event in request_events]
    appended_event_list = current_events_list + request_events
    appended_event_list = np.unique(appended_event_list)

    team.events = ",".join(appended_event_list)
    team.bowlers = ",".join(appended_bowler_list)
    updated_team_serializer = TeamSerializer(team)
    # update team data
    team.save()
    return updated_team_serializer
    # return JsonResponse({"team": updated_team_serializer.data}, status=status.HTTP_201_CREATED)


def updateTeamData(data):
    team_id = data["team_id"]
    updated_bowlers_str = data["bowlers"]
    updated_event_ids_str = data["events"]
    team = checkIfTeamExistInTeamData(team_id)

    if team != None:
        updated_team_serializer = updateExistingTeamData(team, updated_bowlers_str, updated_event_ids_str)
        return (SUCCESS, updated_team_serializer)
    else:
        serializer = TeamSerializer(data=data, many=False)
        if serializer.is_valid():
            serializer.save()
            return (SUCCESS, serializer)
        else:
            return (FAILED, serializer.errors)
            # return JsonResponse({"error": "team data is invalid"}, status=status.HTTP_400_BAD_REQUEST)


def updateEventSummaryData(data, team_id, event_id):
    try:
        current_team_event_summary = EventSummaryData.objects.filter(event_id=event_id).filter(team_id=team_id)
        if len(current_team_event_summary) > 0:
            current_team_event_summary.delete()
    except EventSummaryData.DoesNotExist:
        pass

    eventSummarySerializer = EventSummaryDataSerializer(data=data, many=True)
    if eventSummarySerializer.is_valid():
        eventSummarySerializer.save()
        allEventSummaryData = EventSummaryData.objects.filter(team_id=team_id)

        return (SUCCESS, allEventSummaryData)
        # return JsonResponse({"{team_id}".format(team_id=teamid_request): allEventSummarySerializer.data})
    else:
        return (FAILED, eventSummarySerializer.errors)
        # return JsonResponse({"error": eventSummarySerializer.errors})


def updateTeamEventData(data, team_id, event_id):
    eventdataserializer = EventDataSerializer(data=data, many=True)
    if eventdataserializer.is_valid():
        # If the event id already exist in database, delete all records and updates
        try:
            EventData.objects.filter(team_id=team_id).filter(event_id=event_id).delete()
        except EventData.DoesNotExist:
            pass

        eventdataserializer.save()
        updated_event_data = EventData.objects.filter(team_id=team_id)

        return (SUCCESS, updated_event_data)
        # return JsonResponse({"{team_id}".format(team_id=teamid_request): updated_event_data_serializer.data})
    else:
        return (FAILED, eventdataserializer.errors)
        # return JsonResponse(eventdataserializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)
