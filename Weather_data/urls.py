from django.urls import path
from .views import LatestWeatherData, AddWeatherStations, LatestPM25ActualView, WeatherDataByDate, PM25ActualByDate, LatestPM25PredictionView, PM25PredictionByDate

urlpatterns = [
    path('weather/weatherdata-now/', LatestWeatherData.as_view(http_method_names=['get']), name='weather_data'),
    path('weather/weatherdatabydate/', WeatherDataByDate.as_view(http_method_names=['post']), name='weather_datadate'),
    path('weather/datapm25/', LatestPM25ActualView.as_view(http_method_names=['get']), name='pm25_data'),
    path('weather/datapm25bydate/', PM25ActualByDate.as_view(http_method_names=['post']), name='pm25_datadate'),
    path('weather/datapm25prediction/', LatestPM25PredictionView.as_view(http_method_names=['get']), name='pm25_dataprediction'),
    path('weather/datapm25predictionbydate/', PM25PredictionByDate.as_view(http_method_names=['post']), name='pm25_datapredictiondate'),
    #path('weather/add/', AddWeatherStations.as_view(), name='weather_data'),
]
