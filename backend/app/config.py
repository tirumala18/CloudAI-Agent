import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "eu-west-2")
ASSUME_ROLE_ARN = os.getenv("ASSUME_ROLE_ARN", "")
USE_LOCAL_CREDENTIALS = True
