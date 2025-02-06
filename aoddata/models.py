from django.contrib.gis.db import models

class RasterData(models.Model):
    id = models.AutoField(primary_key=True) 
    raster = models.RasterField(help_text="Data raster GeoTIFF yang disimpan dalam PostGIS")
