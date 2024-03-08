import json
from utils import login


def update_geosession():
    with open("data/auth_data.json", "r") as file:
        data = json.load(file)
    data['geosession'] = login()

    with open("data/auth_data.json", 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    update_geosession()
