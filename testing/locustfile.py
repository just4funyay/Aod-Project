from locust import HttpUser, task, between

class PM25FullAPITest(HttpUser):
    wait_time = between(1, 2)

    # Testing api1
    @task(1)
    def get_aod_today(self):
        self.client.get("/api1/get-data-aod/")

    @task(1)
    def post_aod_by_date(self):
        self.client.post("/api1/get-data-aodbydate/", json={"tanggal": "2025-05-10"})

    @task(1)
    def get_pm25_today(self):
        self.client.get("/api1/get-data-pm25/")

    @task(1)
    def post_pm25_by_date(self):
        self.client.post("/api1/get-data-pm25bydate/", json={"tanggal": "2025-05-10"})

    # testing api2
    @task(1)
    def get_pm25_actual_today(self):
        self.client.get("/api2/weather/datapm25/")

    @task(1)
    def post_pm25_actual_by_date(self):
        self.client.post("/api2/weather/datapm25bydate/", json={"date": "2025-05-10"})

    @task(1)
    def get_weather_today(self):
        self.client.get("/api2/weather/weatherdata-now/")

    @task(1)
    def post_weather_by_date(self):
        self.client.post("/api2/weather/weatherdatabydate/", json={"date": "2025-05-17"})
