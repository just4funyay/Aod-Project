from django.urls import path
from .views import InputDatabase,GetRasterDataView

urlpatterns = [
    path('convert-nc-file/', InputDatabase.as_view(), name='InputDatabase'),
     path('tiles/', GetRasterDataView.as_view(), name='raster_tile'),
]
