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
from datetime import datetime, timedelta

class InputDatabase(APIView):
    def get(self, request):
        today = datetime.today()
        nc_folder_path = os.path.join(settings.BASE_DIR, 'Aod_data/aod-file')

        if not os.path.exists(nc_folder_path):
            return Response(
                {"error": f"Folder {nc_folder_path} tidak ditemukan."},
                status=status.HTTP_404_NOT_FOUND
            )

        geotiff_folder = os.path.join(settings.MEDIA_ROOT, 'geotiff_files')
        if not os.path.exists(geotiff_folder):
            os.makedirs(geotiff_folder)

        processed_files = []
        errors = []

        # Iterasi semua file .nc dalam folder
        for nc_file_name in os.listdir(nc_folder_path):
            if nc_file_name.endswith('.nc'):
                nc_file_path = os.path.join(nc_folder_path, nc_file_name)
                geotiff_file_path = os.path.join(geotiff_folder, nc_file_name.replace('.nc', '.tif'))

                try:
                    # Konversi NC ke GeoTIFF
                    convert_to_geoTiFF_input_data(nc_file_path, geotiff_file_path)
                    raster = GDALRaster(geotiff_file_path, write=True)
                    raster_data = RasterData(raster=raster, time_retrieve=today)
                    raster_data.save()
                    raster = None

                    import gc
                    gc.collect()

                    if os.path.exists(geotiff_file_path):
                        os.remove(geotiff_file_path)
                        print(f"File {geotiff_file_path} berhasil dihapus.")

                    processed_files.append(nc_file_name)
                except Exception as e:
                    errors.append({nc_file_name: str(e)})

        # Kembalikan respons hasil proses
        return Response(
            {
                "processed_files": processed_files,
                "errors": errors if errors else "Semua file berhasil diproses."
            },
            status=status.HTTP_200_OK if not errors else status.HTTP_206_PARTIAL_CONTENT
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