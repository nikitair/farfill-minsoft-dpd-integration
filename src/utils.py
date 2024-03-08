import json
import requests


def login():
    with open("data/auth_data.json", "r") as file:
        data = json.load(file)
    auth_token = data["auth_token"]

    login_endpoint = "https://api.dpd.co.uk/user/?action=login"
    login_headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(login_endpoint, headers=login_headers)
    response.raise_for_status()

    login_data = response.json()["data"]
    return login_data["geoSession"]


def save_to_backup(data):
    backup_file = "data/backups.json"
    with open(backup_file, "w") as f:
        json.dump(data, f, indent=4)
