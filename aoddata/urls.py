from django.urls import path
from .views import InputDatabase,GetRasterDataView

urlpatterns = [
    path('input-database/', InputDatabase.as_view(), name='InputDatabase'),
     path('tiles/', GetRasterDataView.as_view(), name='raster_tile'),
]
