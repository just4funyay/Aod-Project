from ftplib import FTP
from datetime import datetime,timedelta
import os
import requests
from Aod_data.utils import process_himawari_data

def getDataHimawari():
    ftpUser = os.getenv('USERHIMAWARI')
    ftpPassword = os.getenv('PASSHIMAWARI')
    today = datetime.utcnow()
    year = today.year
    month = today.month
    endyear = today.year
    yesterday = today - timedelta(days=1)
    dirData = f"pub/himawari/L3/ARP/031/{year}{month:02d}"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder_name = 'aod-file/Himawari'
    download_path = os.path.join(base_dir, folder_name)
    folder_daily = f"daily"

    ftp = FTP("ftp.ptree.jaxa.jp")
    ftp.login(ftpUser, ftpPassword)
    print("Logged in to FTP server.")
    try:
        ftp.cwd(dirData)
        if folder_daily not in ftp.nlst():
            ftp.cwd('/')
            yesterday_year = yesterday.year
            yesterday_month = yesterday.month
            dirData = f"pub/himawari/L3/ARP/031/{yesterday_year}{yesterday_month:02d}/daily"
            ftp.cwd(dirData)
            
        elif folder_daily in ftp.nlst():
            ftp.cwd('/')
            dirData = f"pub/himawari/L3/ARP/031/{year}{month:02d}/daily"
            ftp.cwd(dirData)
        
        files = sorted(ftp.mlsd())
        print(f"Isi folder {dirData}:")
        
        for file_name, _ in files:
            print(file_name)  
        lastestFile = files[-1][0]
        local_file_path = os.path.join(download_path, lastestFile)
        if lastestFile.endswith('.nc'):
            with open(local_file_path, 'wb') as local_file:
                ftp.retrbinary(f"RETR {lastestFile}", local_file.write)
            print(f"File {lastestFile} berhasil didownload.")
        
    except Exception as e:
        print(f"Gagal mengakses {dirData}: {e}")
    ftp.quit()
    check = process_himawari_data()
    print(check)
