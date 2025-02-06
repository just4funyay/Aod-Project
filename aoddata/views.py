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
            # Menggunakan Raster untuk menyimpan GeoTIFF ke database
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

class GetRasterDataView(APIView):
    def get(self, request):
        
        try:
            connection = psycopg2.connect(
                dbname='aod-project', user='postgres', password='mandaika', host='localhost', port='5432'
            )
            cursor = connection.cursor()

            
            query = """
                SELECT ST_AsTIFF(raster)
                FROM public.aoddata_rasterdata
                WHERE ST_Intersects(raster, ST_MakeEnvelope(100.6, -10.5, 110.0, 0.00, 4326))
            """
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                tile_data = result[0]  
                return Response(tile_data, content_type='image/tiff')
            else:
                return JsonResponse(
                    {"error": "Data raster tidak ditemukan."},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return JsonResponse(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()