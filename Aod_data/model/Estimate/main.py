import os
import sys
import django
import pandas as pd
import csv
import math

# Setup Django environment
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Aod_project.settings")
django.setup()

from .predict import predict_model
from Aod_data.models import RasterData, pm25DataEstimate, PolygondataPM25
from Weather_data.models import WeatherData
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings
from .csvToRaster import csv_to_geotiff, csvToPolygon

folderpath = 'Aod_data/model/Estimate'
os.makedirs(folderpath, exist_ok=True)


def euclidean_distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

def estimatePm25():
    rasterdata_all = RasterData.objects.all()

    for rasterdata in rasterdata_all:
        aod_value = rasterdata.data
        aod_date = rasterdata.time_retrieve

        if pm25DataEstimate.objects.filter(aodid=rasterdata).exists():
            print(f"[SKIP] Data PM2.5 untuk RasterData ID {rasterdata.id} sudah ada.")
            continue

        # Ambil semua data WeatherData beserta lokasi stasiun untuk tanggal yang sama
        all_weather = WeatherData.objects.filter(date=aod_date).select_related('station')
        if not all_weather.exists():
            print(f"[WARNING] Tidak ada data cuaca untuk tanggal {aod_date}, lewati ID {rasterdata.id}.")
            continue

        all_stations = []
        for w in all_weather:
            all_stations.append({
                'station_id': w.station.id,
                'location_x': w.station.location.x,
                'location_y': w.station.location.y,
            })

        merged_rows = []

        for aod in aod_value:
            aod_lon = aod['longitude']
            aod_lat = aod['latitude']
            aod_val = aod['aod_values']

            # Cari stasiun terdekat dengan jarak Euclidean koordinat (lat, lon)
            min_dist = None
            nearest_station_id = None
            for station in all_stations:
                station_lon = station['location_x']
                station_lat = station['location_y']
                dist = euclidean_distance(aod_lat, aod_lon, station_lat, station_lon)
                if (min_dist is None) or (dist < min_dist):
                    min_dist = dist
                    nearest_station_id = station['station_id']

            # Ambil data cuaca stasiun terdekat
            weather_data = WeatherData.objects.filter(date=aod_date, station_id=nearest_station_id).first()
            if not weather_data:
                continue

            merged_rows.append({
                'datetime': aod_date,
                'aod_longitude': aod_lon,
                'aod_latitude': aod_lat,
                'station_longitude': weather_data.station.location.x,
                'station_latitude': weather_data.station.location.y,
                'AOD': aod_val,
                'tempmax': weather_data.temp_max,
                'tempmin': weather_data.temp_min,
                'temp': weather_data.temperature,
                'feelslikemax': weather_data.feels_like_max,
                'feelslikemin': weather_data.feels_like_min,
                'feelslike': weather_data.feels_like,
                'dew': weather_data.dew_point,
                'humidity': weather_data.humidity,
                'precip': weather_data.precipitation,
                'precipcover': weather_data.precip_cover,
                'windgust': weather_data.wind_gust,
                'windspeed': weather_data.wind_speed,
                'winddir': weather_data.wind_dir,
                'sealevelpressure': weather_data.sea_level_pressure,
                'cloudcover': weather_data.cloud_cover,
                'visibility': weather_data.visibility,
                'solarradiation': weather_data.solar_radiation,
                'solarenergy': weather_data.solar_energy,
                'uvindex': weather_data.uv_index,
            })

        if not merged_rows:
            print(f"[WARNING] Tidak ada data gabungan untuk ID {rasterdata.id}, lewati.")
            continue

        # Simpan data gabungan ke CSV
        folderpath = os.path.join(settings.BASE_DIR, 'Aod_data','model','Estimate')
        os.makedirs(folderpath, exist_ok=True)
        file_name = os.path.join(folderpath, f'aod_data_{rasterdata.id}.csv')

        with open(file_name, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=merged_rows[0].keys())
            writer.writeheader()
            writer.writerows(merged_rows)

        print(f"[INFO] Data AOD ID {rasterdata.id} disimpan ke {file_name}")

        df = predict_model(file_name)
        print(df.shape, len(rasterdata.data))

        data = df.to_dict(orient="records")
        jakarta_geojson = os.path.join(settings.BASE_DIR, 'id-jk.geojson')
        polygondata = csvToPolygon(df, jakarta_geojson)

        #pm25data = pm25DataEstimate.objects.create(
        #    aodid=rasterdata,
        #    valuepm25=data,
        #    time=rasterdata.time_retrieve
        #)

        for _, row in polygondata.iterrows():
            geom = row.geometry
            if geom.geom_type == 'MultiPolygon':
                for poly in geom.geoms:
                    polygon = GEOSGeometry(poly.wkt, srid=4326)
                    PolygondataPM25.objects.create(
                        pm25id=pm25data,
                        geom=polygon,
                        pm25_value=row['pm25'],
                        date=pm25data.time
                    )
            else:
                polygon = GEOSGeometry(geom.wkt, srid=4326)
                PolygondataPM25.objects.create(
                    pm25id=pm25data,
                    geom=polygon,
                    pm25_value=row['pm25'],
                    date=pm25data.time
                )

        print(f"[SUCCESS] Prediksi PM2.5 untuk ID {rasterdata.id} disimpan ke database.\n")

        # Hapus file CSV setelah proses selesai
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"File {file_name} berhasil dihapus.")
        else:
            print(f"File {file_name} tidak ditemukan.")


estimatePm25()