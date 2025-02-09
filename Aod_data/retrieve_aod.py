import earthaccess
import pathlib
from datetime import datetime, timedelta

def retrieve_viirs_data():
    today = datetime.today()
    yesterday = today - timedelta(days=3)

    today = today.strftime("%Y-%m-%d")
    yesterday = yesterday.strftime("%Y-%m-%d")

    cwd = pathlib.Path.cwd()

    auth = earthaccess.login(strategy="netrc")

    # 2. Search
    results = earthaccess.search_data(
        short_name='AERDB_L2_VIIRS_SNPP',  
        bounding_box=(106.5, -6.5, 107.1, -6),  
        temporal=(yesterday, today)
    )

    folder_name = 'aod-file'
    download_path = cwd / folder_name
    print(download_path)
    # 3. Access
    files = earthaccess.download(results, download_path)