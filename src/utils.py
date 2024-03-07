import json
import requests



def save_to_backup(data):
    backup_file = "data/backups.json"
    with open(backup_file, "w") as f:
        json.dump(data, f, indent=4)


def retrieve_geosession_token(api_key):
    """
    Function to retrieve a new Geosession token from the geolocation service's API.

    Parameters:
        api_key (str): Your API key for the geolocation service.

    Returns:
        str: The obtained Geosession token.
    """
    response = requests.get('https://geolocation-service.com/token',
                            params={'key': api_key})

    if response.status_code == 200:
        return response.json().get('token')
    else:
        response.raise_for_status()


if __name__ == '__main__':
    api_key = 'YOUR_API_KEY'

    # Retrieve Geosession token
    geosession_token = retrieve_geosession_token(api_key)
    print("Retrieved Geosession token:", geosession_token)

