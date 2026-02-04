import os
import boto3
from app.config import ASSUME_ROLE_ARN, USE_LOCAL_CREDENTIALS

def assume_role():
    """
    Returns a boto3 session.
    If USE_LOCAL_CREDENTIALS is True, it uses direct access keys from env variables.
    Otherwise, it assumes the role defined in ASSUME_ROLE_ARN.
    """
    if USE_LOCAL_CREDENTIALS:
        # Use direct keys from environment variables
        access_key = os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        session_token = os.getenv("AWS_SESSION_TOKEN")  # Optional, only for temporary creds

        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=session_token
        )
    else:
        # Assume role
        sts = boto3.client("sts")
        creds = sts.assume_role(
            RoleArn=ASSUME_ROLE_ARN,
            RoleSessionName="cloud-agent-session"
        )["Credentials"]

        session = boto3.Session(
            aws_access_key_id=creds["AccessKeyId"],
            aws_secret_access_key=creds["SecretAccessKey"],
            aws_session_token=creds["SessionToken"]
        )

    return session


