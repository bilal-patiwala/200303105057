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
    current_time = datetime.datetime.now().time()
    # filtering train hich are not departing in next 30 minutes
    filtered_data = [train for train in data if not is_departing_soon(train['departureTime'], current_time)]

    # sortinf filtering data
    sorted_data = sorted(filtered_data, key=lambda nd:(
        nd['price']['AC'],
        nd['price']['sleeper'],
        -nd['seatsAvailable']['AC'],
        -nd['seatsAvailable']['sleeper'],
        -nd['departureTime']['Hours'],
        -(nd['departureTime']['Minutes'] - nd['delayedBy'])
    ))
    return JsonResponse(sorted_data, safe=False)

@api_view(['GET'])
def getSpecificTrain(request, trainNo):
    authorization = request.headers.get('Authorization')
    url = f'http://20.244.56.144/train/trains/{trainNo}'
    headers = {
        "Authorization" : authorization
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return JsonResponse(data=data, safe=False)

def is_departing_soon(departure_time, current_time):
    departure = datetime.time(departure_time['Hours'], departure_time['Minutes'], departure_time['Seconds'])
    time_difference = datetime.datetime.combine(datetime.date.today(), departure) - datetime.datetime.combine(datetime.date.today(), current_time)
    return time_difference.total_seconds() <= 1800