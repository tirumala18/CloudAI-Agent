from fastapi import APIRouter, HTTPException
from app.models.schemas import CommandRequest
from app.agent import run_agent
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/execute")
def execute(request: CommandRequest):
    """
    Main endpoint. Receives a natural language query from the UI,
    runs it through the LangChain agent, returns a human-friendly response.
    """
    if not request.command or not request.command.strip():
        raise HTTPException(status_code=400, detail="Command cannot be empty.")

    try:
        answer = run_agent(request.command, account_id=request.account_id)
        return {"response": answer}
    except Exception as e:
        logger.exception(f"Error executing command: {request.command}")
        raise HTTPException(status_code=500, detail=f"Backend error: {str(e)}")
