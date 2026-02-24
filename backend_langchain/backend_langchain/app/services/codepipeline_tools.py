import boto3
from langchain.tools import tool
from app.aws_client import get_boto_client


def _get_pipeline_overall_status(pipeline_name: str) -> dict:
    cp = get_boto_client("codepipeline")
    state = cp.get_pipeline_state(name=pipeline_name)
    executions = []
    for stage in state["stageStates"]:
        exc = stage.get("latestExecution")
        if exc:
            executions.append(exc)

    if not executions:
        return {}

    priority = {"Failed": 3, "InProgress": 2, "Succeeded": 1}
    overall = max(executions, key=lambda e: priority.get(e["status"], 0))
    return {
        "status": overall["status"],
        "lastStatusChange": str(overall.get("lastStatusChange", ""))
    }


def _get_pipeline_source(pipeline_name: str) -> dict:
    cp = get_boto_client("codepipeline")
    pipeline = cp.get_pipeline(name=pipeline_name)
    for stage in pipeline["pipeline"]["stages"]:
        if stage["name"].lower() == "source":
            action = stage["actions"][0]
            cfg = action["configuration"]
            return {
                "provider": action["actionTypeId"]["provider"],
                "repo": cfg.get("FullRepositoryId"),
                "branch": cfg.get("BranchName"),
            }
    return {}


def _get_commit_id(pipeline_name: str) -> str:
    cp = get_boto_client("codepipeline")
    state = cp.get_pipeline_state(name=pipeline_name)
    for stage in state["stageStates"]:
        if stage["stageName"].lower() == "source":
            for action in stage.get("actionStates", []):
                exc = action.get("latestExecution", {})
                return exc.get("externalExecutionId", "N/A")
    return "N/A"


@tool
def get_pipeline_status(pipeline_name: str) -> str:
    """
    Get the full status of a CodePipeline — including current status,
    branch, latest commit ID, and source repository.
    Input: pipeline name, e.g. 'payments-prod-pipeline'
    """
    try:
        status = _get_pipeline_overall_status(pipeline_name)
        source = _get_pipeline_source(pipeline_name)
        commit = _get_commit_id(pipeline_name)

        return (
            f"Pipeline: {pipeline_name}\n"
            f"  Status:     {status.get('status', 'Unknown')}\n"
            f"  Last run:   {status.get('lastStatusChange', 'N/A')}\n"
            f"  Branch:     {source.get('branch', 'N/A')}\n"
            f"  Repository: {source.get('repo', 'N/A')}\n"
            f"  Provider:   {source.get('provider', 'N/A')}\n"
            f"  Commit ID:  {commit}"
        )
    except Exception as e:
        if "PipelineNotFoundException" in str(type(e)):
            return f"Pipeline '{pipeline_name}' not found."
        return f"Error fetching pipeline status: {str(e)}"


@tool
def list_pipelines(query: str = "") -> str:
    """
    List all CodePipelines in the AWS account.
    Use this when the developer doesn't know the exact pipeline name.
    """
    try:
        cp = get_boto_client("codepipeline")
        response = cp.list_pipelines()
        pipelines = [p["name"] for p in response.get("pipelines", [])]
        if not pipelines:
            return "No pipelines found."
        return "Available Pipelines:\n" + "\n".join(f"  - {p}" for p in pipelines)
    except Exception as e:
        return f"Error listing pipelines: {str(e)}"
