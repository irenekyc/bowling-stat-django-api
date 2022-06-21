# create endpoint
from django.http import JsonResponse
from rest_framework.response import Response
from .models import Team, EventData
from .serializers import TeamSerializer, EventDataSerializer
from rest_framework import status
from rest_framework.decorators import api_view
import numpy as np
from .utlis import *
from .names import *


def team_list(self):
  teams = []
  # get all teams
  teams = Team.objects.all()
  # serialize team data
  serializer = TeamSerializer(teams, many=True)

  # return json  
  return JsonResponse({"teams":serializer.data}, safe=False)

@api_view(['GET', 'POST'])
def add_team(request, **arg):
  if request.method == 'GET':
    return JsonResponse({"error": "API route does not exist"},status=status.HTTP_404_NOT_FOUND)

  if request.method == 'POST':
    # do something
    data = request.data
    # serializer = TeamSerializer(data=data)
    (addStatus, response) = updateTeamData(data=data)
    if addStatus == SUCCESS:
      return JsonResponse({"team": response.data}, status=status.HTTP_201_CREATED)
    else: 
      return JsonResponse({"error": response}, status=status.HTTP_400_BAD_REQUEST)




def team_data(self, **arg):
  teamid_request = arg['teamid']
  print(teamid_request)
  if teamid_request == None:
    return JsonResponse({"team":{}}, safe=False)
  else:
    try:
      team = Team.objects.get(team_id=teamid_request)
    except Team.DoesNotExist:
      team = None


    if team:
      serializer = TeamSerializer(team, many=False)
      return JsonResponse(serializer.data, safe=False)
    else:
      return JsonResponse({"error": "Team does not exist"},status=status.HTTP_404_NOT_FOUND)
 


def team_events_all(self, **args):
  teamid_request = args['teamid']
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


@api_view(['GET', 'POST'])
def add_team_event_data(request, **args):
    if request.method == 'GET':
      return JsonResponse({"error": "API route does not exist"},status=status.HTTP_404_NOT_FOUND)
    
    teamid_request = request.query_params.get('team')
    eventid_request = request.query_params.get('event')
    if request.method == 'POST':
      # do something
      data = request.data
      eventdataserializer = EventDataSerializer(data=data, many=True)
      if eventdataserializer.is_valid():
          # If the event id already exist in database, delete all records and updates
          try:
            EventData.objects.filter(team_id=teamid_request).filter(event_id=eventid_request).delete()
          except EventData.DoesNotExist:
            pass
          eventdataserializer.save()
          updated_event_data = EventData.objects.filter(team_id=teamid_request)
          updated_event_data_serializer = EventDataSerializer(updated_event_data, many=True)

          team_name = updated_event_data[0].team_name

          # get all bowlers from the data
          bowlers = []
          for event_entry in data:
            bowlers.append(event_entry['bowler'])
          bowlers = np.unique(bowlers)
  
          (status,_) = updateTeamData(data={
            "team_id":teamid_request,
            "team_name": team_name,
            "bowlers": ",".join(bowlers),
            "events": eventid_request
          })
          if status == SUCCESS:
            # do somthing
            pass
          else:
            #do somthing
            pass

          return JsonResponse({"{team_id}".format(team_id=teamid_request): updated_event_data_serializer.data})
      else: 
         return JsonResponse(eventdataserializer.errors, status=status.HTTP_400_BAD_REQUEST,safe=False)
