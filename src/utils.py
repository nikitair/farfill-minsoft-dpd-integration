import json
import requests
from fastapi import Request
from logs.logging_config import logger
from datetime import datetime

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


async def backup_request(request: Request, response):
    logger.info(f"{backup_request.__name__} -- BACKING UP REQUEST")

    all_backups = []

    try:
        with open("data/backups.json", "r") as f:
            all_backups = json.load(f)
    except Exception:
        logger.exception(f"{backup_request.__name__} -- !!! ERROR LOADING BACKUPS JSON")
    
    if isinstance(all_backups, list):
        logger.info(f"{backup_request.__name__} -- {len(all_backups)} RECEIVED")

    result = {
        "ip": None,
        "url": None,
        "base_url": None,
        "headers": None,
        "request": None,
        "response": response,
        "created_at": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S UTC')
    }

    try:
        result["ip"] = request.client.host
        result["url"] = request.url
        result["base_url"] = request.base_url
        result["headers"] = request.headers
        result["request"] = await request.json()
    except Exception:
        logger.exception(f"{backup_request.__name__} -- !!! ERROR PARSING REQUEST")

    logger.info(f"{backup_request.__name__} -- PREPARED BACKUP - {result}")

    with open("data/backups.json", "w") as f:
        all_backups.append(result)
        json.dump(all_backups, f)

    logger.info(f"{backup_request.__name__} -- BACKUP SAVED")
    return True

    
