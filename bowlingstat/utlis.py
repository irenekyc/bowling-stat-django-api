from .models import Team
from django.http import JsonResponse
from .serializers import TeamSerializer, EventDataSerializer
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
        print('team data exist')
        # get bowlers
        current_bowler_list = team.bowlers.split(",")
        current_bowler_list = [bowler.strip() for bowler in current_bowler_list]
        request_bowlers = updated_bowlers_str.split(",")
        request_bowlers = [bowler.strip() for bowler in request_bowlers]
        appended_bowler_list = current_bowler_list +request_bowlers
        appended_bowler_list = np.unique(appended_bowler_list)
      
        # get events
        current_events_list = team.events.split(",")
        current_events_list = [events.strip() for events in current_events_list]
        request_events = updated_event_ids_str.split(",")
        request_events = [event.strip() for event in request_events]
        appended_event_list = current_events_list +request_events
        appended_event_list = np.unique(appended_event_list)

        team.events = ",".join(appended_event_list)
        team.bowlers = ",".join(appended_bowler_list)
        updated_team_serializer = TeamSerializer(team)
        # update team data
        team.save()
        return updated_team_serializer
        # return JsonResponse({"team": updated_team_serializer.data}, status=status.HTTP_201_CREATED)

def updateTeamData(data):
    team_id = data['team_id']
    updated_bowlers_str = data['bowlers']
    updated_event_ids_str = data['events']
    team = checkIfTeamExistInTeamData(team_id)
  
    if team != None:
        updated_team_serializer = updateExistingTeamData(team, updated_bowlers_str, updated_event_ids_str)
        return (SUCCESS, updated_team_serializer)
    else: 
      serializer = TeamSerialzer(data, many=False)
      if serializer.is_valid():
        serializer.save()
        return (SUCCESS, serializer)
      else: 
        return(FAILED, serializer.errors)
          # return JsonResponse({"error": "team data is invalid"}, status=status.HTTP_400_BAD_REQUEST)
