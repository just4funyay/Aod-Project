from django.contrib.gis.db import models
# Sementara 2 kolom
class RasterData(models.Model):
    id = models.AutoField(primary_key=True) 
    raster = models.RasterField()
