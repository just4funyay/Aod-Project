from django.urls import path
from .views import FetchWeatherDataView

urlpatterns = [
    path('get-weather-today/', FetchWeatherDataView.as_view(), name='weather-data'),
]
