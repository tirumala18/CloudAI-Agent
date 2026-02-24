from pydantic import BaseModel

class CommandRequest(BaseModel):
    command: str
    params: dict | None = None
    account_id: str | None = None
