from pydantic import BaseModel

class CommandRequest(BaseModel):
    command: str
    params: dict | None = None
