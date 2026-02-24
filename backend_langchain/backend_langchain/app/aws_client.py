import boto3
from app.context import current_account_id
import logging

logger = logging.getLogger(__name__)

def get_boto_client(service_name: str, region_name: str = None):
    account_id = current_account_id.get()
    if account_id and account_id != 'default':
        try:
            sts = boto3.client('sts')
            role_arn = f'arn:aws:iam::{account_id}:role/CloudAgentAccessRole'
            logger.info(f'Assuming role {role_arn} for {service_name}')
            resp = sts.assume_role(RoleArn=role_arn, RoleSessionName='CloudAgentSession')
            creds = resp['Credentials']
            return boto3.client(
                service_name,
                aws_access_key_id=creds['AccessKeyId'],
                aws_secret_access_key=creds['SecretAccessKey'],
                aws_session_token=creds['SessionToken'],
                region_name=region_name
            )
        except Exception as e:
            logger.error(f'Failed to assume role for account {account_id}, using default account fallback! Error: {e}')
            return boto3.client(service_name, region_name=region_name)
    return boto3.client(service_name, region_name=region_name)