from django.db import models

class WeatherData(models.Model):
    location = models.CharField(max_length=100)
    datetime = models.DateField()  # Data waktu yang diambil dari Visual Crossing
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    precipitation = models.FloatField()

    def __str__(self):
        return f"Weather in {self.location} at {self.datetime}"
