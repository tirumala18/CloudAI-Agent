import requests

def map_to_command(user_input: str):
    prompt = f"""
    You are an AWS assistant.

    Convert the user request into ONE command:
    - list-s3
    - describe-ec2

    Output ONLY the command name.

    User: "{user_input}"
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt}
    )
    
    text = ""
    for line in response.iter_lines():
        if line:
            data = line.decode("utf-8")
            if '"response"' in data:
                text += data.split('"response":"')[1].split('"')[0]

    return text.strip().lower()
