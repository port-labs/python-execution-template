import logging
from typing import Literal, Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_permission(aws_account: str) -> Union[Literal['FAILURE'], Literal['SUCCESS']]:
    try:
        # Your code goes here
        return 'SUCCESS'
    except Exception as err:
        logger.error(f"init add permission failed {err}")

    return 'FAILURE'
