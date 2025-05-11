from django.urls import path
from .views import WeatherDataListView, WeatherFetchView, AddWeatherStations, WeatherFetchViewRange,LatestPM25ActualView

urlpatterns = [
    path('weather/fetch/', WeatherFetchView.as_view(), name='fetch_weather'),
    path('weather/fetch-range/', WeatherFetchViewRange.as_view(), name='fetch_weather'),
    path('weather/data/', WeatherDataListView.as_view(), name='weather_data'),
    path('weather/add/', AddWeatherStations.as_view(), name='weather_data'),
    path('weather/datapm25/', LatestPM25ActualView.as_view(), name='weather_data'),
]
