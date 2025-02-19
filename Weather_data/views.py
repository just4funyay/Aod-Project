import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import WeatherData
from .serializers import WeatherDataSerializer
from datetime import date

class FetchWeatherDataView(APIView):
    API_KEY = "KTJ63YA3XS9PHPBWTWHKAR5D8"  # Ganti dengan API Visual Crossing
    LOCATION = "Jakarta"
    BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    
    def get(self, request):
        # Fetch weather data
        api_url = f"{self.BASE_URL}{self.LOCATION}?unitGroup=metric&key={self.API_KEY}&include=current"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            current_data = data.get('currentConditions', {})
            
            # Extract required data
            temperature = current_data.get('temp')
            humidity = current_data.get('humidity')
            wind_speed = current_data.get('windspeed')
            datetime = date.today()
            precipitation = current_data.get('precip')
            if precipitation == None:
                precipitation = 0
            
            # Save to database
            weather_entry = WeatherData(
                temperature=temperature,
                humidity=humidity,
                wind_speed=wind_speed,
                datetime=datetime,
                precipitation=precipitation
            )
            weather_entry.save()

            # Serialize and return the response
            serializer = WeatherDataSerializer(weather_entry)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"error": "Failed to fetch weather data"}, status=status.HTTP_400_BAD_REQUEST)
