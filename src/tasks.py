import json
import schedule
import time

from utils import login


def update_geosession():
    with open("data/auth_data.json", "r") as file:
        data = json.load(file)
    data['geosession'] = login()

    with open("data/auth_data.json", 'w') as file:
        json.dump(data, file, indent=4)


schedule.every().day.at("06:00").do(update_geosession)


def run_geosession_processing():
    while True:
        schedule.run_pending()
        time.sleep(1)
