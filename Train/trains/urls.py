from django.urls import path
from . import views

urlpatterns = [
    path("trains", views.getTrains, name="getTrains"),
    path('trains/<str:trainNo>', views.getSpecificTrain, name="getParticularTrain")
]