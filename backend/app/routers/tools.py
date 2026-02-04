from fastapi import APIRouter, HTTPException
from app.agent import interpret_command
from app.services import aws_tools
from app.models.schemas import CommandRequest
from app.extractors import extract_pipeline_name
from app.services.codepipeline_tools import get_pipeline_info
from fastapi import HTTPException


router = APIRouter()

@router.post("/execute")
def execute(request: CommandRequest):
    command = interpret_command(request.command)

    if command == "list-s3":
        return aws_tools.list_s3()

    if command == "codepipeline-status":
        pipeline = extract_pipeline_name(request.command)
        if not pipeline:
            raise HTTPException(400, "Pipeline name not found")

        return get_pipeline_info(pipeline)    

    raise HTTPException(
        status_code=400,
        detail=f"Unable to map command: {request.command}"
    )

