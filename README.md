# Aod-Project

Perlu install OsGeo4w untuk kebutuhan dependencies GeoDjango [halaman unduhan OSGeo4W](https://trac.osgeo.org/osgeo4w/).
Selanjutnya konfigurasi disini [Panduan Instalasi Django GIS](https://docs.djangoproject.com/en/5.1/ref/contrib/gis/install/)

Terdapat 4 Folder:
- [aod-file](https://github.com/just4funyay/Aod-Project/tree/main/aod-file), folder ini menampung file .nc sementara sebelum pre-processing.
- [aod](https://github.com/just4funyay/Aod-Project/tree/main/aod), folder proyek utama
- [aoddata](https://github.com/just4funyay/Aod-Project/tree/main/aoddata), folder app
- [media](https://github.com/just4funyay/Aod-Project/tree/main/aoddata), folder penampungan sementara hasil konversi file.nc menjadi file.tiff

Database perlu install ekstensi postgis dan postgis_raster

Pengembangan sejauh ini masih bersifat satu file saja

Sementara untuk proses input Database Hit melalui Endpoint localhost:8000/api/input-database
