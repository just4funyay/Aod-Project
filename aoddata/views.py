from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from django.conf import settings
from .utils import convert_to_geoTiFF_input_data
import psycopg2
from django.http import JsonResponse
from .models import RasterData
from django.core.files import File
from django.contrib.gis.gdal import GDALRaster

class InputDatabase(APIView):
    def get(self, request):
        nc_file_name = "AERDB_L2_VIIRS_SNPP.A2023255.0636.002.2023255185945.nc"  
        nc_file_path = os.path.join(settings.BASE_DIR, 'aod-file', nc_file_name)

        if not os.path.exists(nc_file_path):
            return Response(
                {"error": f"File {nc_file_name} tidak ditemukan."},
                status=status.HTTP_404_NOT_FOUND
            )

        geotiff_folder = os.path.join(settings.MEDIA_ROOT, 'geotiff_files')
        if not os.path.exists(geotiff_folder):
            os.makedirs(geotiff_folder)

        geotiff_file_path = os.path.join(geotiff_folder, nc_file_name.replace('.nc', '.tif'))
        print(geotiff_file_path)

        # Konversi NC ke GeoTIFF
        try:
            geoTIFF_files = convert_to_geoTiFF_input_data(nc_file_path, geotiff_file_path)
            print(geoTIFF_files)
            raster = GDALRaster(geotiff_file_path, write=True)
            raster_data = RasterData(raster=raster)
            return Response(
                {"message": f"File {nc_file_name} berhasil diproses dan disimpan ke database."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# class GetRasterDataView(APIView):
    # Sedang Pengerjaan
