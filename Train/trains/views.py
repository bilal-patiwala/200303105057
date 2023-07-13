from django.shortcuts import render
from django.http import JsonResponse
import requests
from rest_framework.decorators import api_view
import datetime

# Create your views here.
@api_view(['GET'])
def getTrains(request):
    authorization = request.headers.get('Authorization')
    url = "http://20.244.56.144/train/trains"
    headers = {
        "Authorization" : authorization
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    
    filter_data = [train for train in data if not is_departing_soon(train['departureTime'], current_time)]

    return JsonResponse(data, safe=False)


def is_departing_soon(departure_time, current_time):
    departure = datetime.time(departure_time['Hours'], departure_time['Minutes'], departure_time['Seconds'])
    time_difference = datetime.datetime.combine(datetime.date.today(), departure) - datetime.datetime.combine(datetime.date.today(), current_time)
    return time_difference.total_seconds() <= 1800