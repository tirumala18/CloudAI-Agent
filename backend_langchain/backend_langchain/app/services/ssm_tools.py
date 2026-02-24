import boto3
from langchain.tools import tool
from app.aws_client import get_boto_client


@tool
def get_ssm_parameter(parameter_name: str) -> str:
    """
    Fetch an environment variable or config value from AWS SSM Parameter Store.
    Input: full parameter name, e.g. '/prod/payments/DB_HOST' or 'MY_PARAM'
    """
    try:
        ssm = get_boto_client("ssm")
        r = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        value = r["Parameter"]["Value"]
        return f"Parameter: {parameter_name}\nValue: {value}"
    except Exception as e:
        if "ParameterNotFound" in str(type(e)):
            return f"Parameter '{parameter_name}' not found in SSM Parameter Store."
        return f"Error fetching parameter: {str(e)}"


@tool
def list_ssm_parameters(path_prefix: str = "/") -> str:
    """
    List available SSM parameters under a given path prefix.
    Example input: '/prod/payments' to list all payments prod variables.
    """
    try:
        ssm = get_boto_client("ssm")
        r = ssm.get_parameters_by_path(Path=path_prefix, Recursive=True)
        params = r.get("Parameters", [])
        if not params:
            return f"No parameters found under path: {path_prefix}"
        names = [p["Name"] for p in params]
        return f"Parameters under '{path_prefix}':\n" + "\n".join(f"  - {n}" for n in names)
    except Exception as e:
        return f"Error listing parameters: {str(e)}"


@tool
def put_ssm_parameter(input_str: str) -> str:
    """
    Add or update an environment variable in AWS SSM Parameter Store.
    Input format: 'parameter_name|value|environment'
    Example: '/staging/payments/DB_HOST|db.staging.example.com|staging'
    NOTE: Production changes require DevOps approval and will NOT be applied automatically.
    """
    try:
        parts = input_str.strip().split("|")
        if len(parts) != 3:
            return "Invalid format. Use: 'parameter_name|value|environment'"

        name, value, env = parts[0].strip(), parts[1].strip(), parts[2].strip()

        # Safety gate — prod requires human approval
        if "prod" in env.lower() or "prod" in name.lower():
            return (
                f"⚠️  APPROVAL REQUIRED\n"
                f"Parameter: {name}\n"
                f"Requested value: {value}\n"
                f"Environment: {env}\n\n"
                f"Production changes require DevOps team approval.\n"
                f"Please raise this in #devops-approvals on Slack."
            )

        ssm = get_boto_client("ssm")
        ssm.put_parameter(
            Name=name,
            Value=value,
            Type="SecureString",
            Overwrite=True
        )
        return f"✅ Parameter '{name}' updated successfully in {env}."
    except Exception as e:
        return f"Error updating parameter: {str(e)}"
