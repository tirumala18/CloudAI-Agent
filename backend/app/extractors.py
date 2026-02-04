import re

def extract_pipeline_name(text: str):
    """
    Extracts pipeline name from user input.
    Example: 'status of pipeline payments-prod'
    """
    match = re.search(r"pipeline\s+([a-zA-Z0-9-_]+)", text)
    return match.group(1) if match else None

