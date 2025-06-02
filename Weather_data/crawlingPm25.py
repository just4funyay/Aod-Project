import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
from .pm25ToDatabase import pm25ToDatabase
from django.conf import settings
import sys
import requests
from bs4 import BeautifulSoup
import django
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Aod_project.settings")
django.setup()

from datetime import datetime
from Weather_data.models import WeatherStation, pm25DataActual

urls = [
        {"url": "https://rendahemisi.jakarta.go.id/ispu-detail/1/us-embassy-1/", "nama_tempat": "us_embassy_1"},
        {"url": "https://rendahemisi.jakarta.go.id/ispu-detail/2/us-embassy-2/", "nama_tempat": "us_embassy_2"},
        {"url": "https://rendahemisi.jakarta.go.id/ispu-detail/3/jakarta-gbk/", "nama_tempat": "jakarta_gbk"},
        {"url": "https://rendahemisi.jakarta.go.id/ispu-detail/4/dki1-bundaran-hi/", "nama_tempat": "bundaran_hi"},
        {"url": "https://rendahemisi.jakarta.go.id/ispu-detail/5/dki2-kelapa-gading/", "nama_tempat": "kelapa_gading"},
        {"url": "https://rendahemisi.jakarta.go.id/ispu-detail/6/dki3-jagakarsa/", "nama_tempat": "jagakarsa"},
        {"url": "https://rendahemisi.jakarta.go.id/ispu-detail/7/dki4-lubang-buaya/", "nama_tempat": "lubang_buaya"},
        {"url": "https://rendahemisi.jakarta.go.id/ispu-detail/8/dki5-kebun-jeruk/", "nama_tempat": "kebun_jeruk"},
    ]

def get_ispu_pm25_now():
    headers = {"User-Agent": "Mozilla/5.0"}
    for tempat in urls:
        try:
            res = requests.get(tempat["url"], headers=headers)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")

            nilai_pm25 = None
            # Cari semua div dengan class 'feature-box-icon'
            for box_icon in soup.find_all("div", class_="feature-box-icon"):
                p_tag = box_icon.find("p")
                # <p> mengandung "PM 2.5"
                if p_tag and "PM 2.5" in p_tag.text:
                    h5_tag = box_icon.find("h5")
                    if h5_tag:
                        nilai_pm25 = h5_tag.text.strip()
                        break

            # Simpan ke database setelah ditemukan
            if nilai_pm25 is None:
                nilai_pm25 = 0.0
            if nilai_pm25 is not None:
                try:
                    stasiun = WeatherStation.objects.get(name__iexact=tempat['nama_tempat'].strip())
                    tanggal = datetime.now().date()  # objek date
                    pm25DataActual.objects.create(
                        station=stasiun,
                        date=tanggal,
                        pm25_value=float(nilai_pm25)
                    )
                except Exception as e:
                    print(f"Error simpan data {tempat['nama_tempat']}: {e}")

            print(f"{tempat['nama_tempat']}: {nilai_pm25 or 'Tidak ditemukan'}")

        except Exception as e:
            print(f"{tempat['nama_tempat']}: Error - {e}")

def download_ispu_last_40_days():
    output_folder = os.path.join(settings.BASE_DIR, "Weather_data", "data_ispu")
    os.makedirs(output_folder, exist_ok=True)
    download_url = "https://rendahemisi.jakarta.go.id/Page/ExportIspuData"

    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0"}

    for tempat in urls:
        url = tempat["url"]
        nama_tempat = tempat["nama_tempat"]

        # Ambil CSRF token dari halaman tempat
        response = session.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        csrf_token = soup.find("input", {"name": "csrf_binari"})["value"]
        id_location = url.split('/')[4]

        for day in range(30):
            date = datetime.today() - timedelta(days=day)
            formatted_date = date.strftime("%d-%m-%Y")
            file_date = date.strftime("%Y%m%d")
            filename = os.path.join(output_folder, f"{nama_tempat}_{file_date}.xls")

                
            if os.path.exists(filename):
                print(f"[=] Lewati (sudah ada): {filename}")
                continue

            payload = {
                "csrf_binari": csrf_token,
                "id_location": id_location,
                "historical_date": formatted_date
            }

            headers["Referer"] = url
            res_download = session.post(download_url, data=payload, headers=headers)
            res_download.raise_for_status()

            with open(filename, "wb") as f:
                f.write(res_download.content)

            print(f"Berhasil: {filename}")


    pm25ToDatabase(output_folder, "ISPU PM2.5")
