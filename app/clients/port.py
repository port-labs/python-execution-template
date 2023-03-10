import logging
import json
import requests
from typing import Literal, Union

from core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_port_api_token():
    """
    Get a Port API access token
    This function uses CLIENT_ID and CLIENT_SECRET from config
    """

    credentials = {'clientId': settings.PORT_CLIENT_ID,
                   'clientSecret': settings.PORT_CLIENT_SECRET}

    token_response = requests.post(
        f"{settings.PORT_API_URL}/auth/access_token", json=credentials)

    return token_response.json()['accessToken']


def update_action(run_id: str, message: str, status: Union[Literal['FAILURE'], Literal['SUCCESS']]):
    """
    Reports to Port on the status of an action run
    """

    token = get_port_api_token()
    headers = {
        'Authorization': f"Bearer {token}"
    }
    body = {
        'message': {
            'message': message
        },
        'status': status
    }

    if status == 'FAILURE':
        body['status'] = status

    logger.info(f"update action with: {json.dumps(body)}")
    response = requests.patch(
        f"{settings.PORT_API_URL}/actions/runs/{run_id}", json=body, headers=headers)
    logger.info(
        f"update action response - status: {response.status_code}, body: {json.dumps(response.json())}")

    return response.status_code


def create_entity(blueprint: str, properties: dict, relations: dict, run_id: str):
    """
    Create new entity for blueprint in Port
    """

    token = get_port_api_token()
    headers = {
        'Authorization': f"Bearer {token}"
    }
    body = {
        "properties": properties,
        "relations": relations
    }

    logger.info(f"create entity with: {json.dumps(body)}")
    response = requests.post(f"{settings.PORT_API_URL}/blueprints/{blueprint}/entities?run_id={run_id}",
                             json=body, headers=headers)
    logger.info(
        f"create entity response - status: {response.status_code}, body: {json.dumps(response.json())}")

    return response.status_code
