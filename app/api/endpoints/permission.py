import logging
from fastapi import APIRouter, Depends

from actions import add_permission
from api.deps import verify_webhook
from clients import port
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/permission", dependencies=[Depends(verify_webhook)])
async def handle_add_permissions(webhook: Webhook):
    logger.info(f"Webhook body: {webhook}")

    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']
    properties = webhook.payload['properties']
    user_email = webhook.trigger.by.user.email

    if action_type == 'CREATE' and action_identifier == 'requestPermission':
        aws_account = properties['account']
        run_id = webhook.context.runId

        logger.info(f"Assigning new permissions to {aws_account}")

        action_status = add_permission.add_permission(aws_account)

        message = f"The action status after permission creation is {action_status}"
        port.create_entity(
            'permission', {"user": user_email}, properties, run_id)
        port.update_action(run_id, message, action_status)

        return {'status': 'SUCCESS'}

    return {'status': 'IGNORED'}
