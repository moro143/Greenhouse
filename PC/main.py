import requests
import time
from datetime import datetime
import csv
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ.get("INFLUXDB_TOKEN")
org = "moro"
url = "http://localhost:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

ESP_URL = "http://192.168.0.62"  # <-- Replace with your ESP's IP
LOG_FILE = "sensor_log.csv"

bucket = "sensors"


def fetch_data():
    try:
        response = requests.get(ESP_URL, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"[ERROR] {e}")
    return None


def log_to_csv(data):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [now, data["temperature"], data["humidity"], data["soil_moisture"]]
        )
        point = (
            Point("sensor_data")
            .tag("device", "esp_sensor")
            .field("temperature", data["temperature"])
            .field("humidity", data["humidity"])
            .field("soil_moisture", data["soil_moisture"])
        )
        write_client.write_api(write_options=SYNCHRONOUS).write(
            bucket=bucket, org=org, record=point
        )
        print(f"[{now}] Logged: {data}")


def ensure_csv_header():
    try:
        with open(LOG_FILE, "x", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Temperature", "Humidity", "SoilMoisture"])
    except FileExistsError:
        pass  # File already exists


def main():
    ensure_csv_header()
    while True:
        data = fetch_data()
        if data:
            log_to_csv(data)
        else:
            print("[WARN] Failed to get data")
        time.sleep(10)  # Log every 10 seconds


if __name__ == "__main__":
    main()
