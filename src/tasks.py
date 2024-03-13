import json
from time import sleep

from utils import retrieve_geosession_token


@celery_app.task
def update_geosession():
    with open("data/auth_data.json", "r") as file:
        data = json.load(file)
    api_key = "Basic ZmFyZmlsbDpmYXJmaWxsQDEyMw=="
    data['geosession'] = retrieve_geosession_token(api_key)

    with open("data/auth_data.json", 'w') as file:
        json.dump(data, file, indent=4)
