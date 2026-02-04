import boto3

cp = boto3.client("codepipeline")


def get_pipeline_overall_status(pipeline_name):
    state = cp.get_pipeline_state(name=pipeline_name)

    executions = []
    for stage in state["stageStates"]:
        exec = stage.get("latestExecution")
        if exec:
            executions.append(exec)

    if not executions:
        return {}

    # Failed > InProgress > Succeeded
    priority = {
        "Failed": 3,
        "InProgress": 2,
        "Succeeded": 1
    }

    overall = max(executions, key=lambda e: priority.get(e["status"], 0))

    return {
        "status": overall["status"],
        "lastExecutedTime": overall.get("lastStatusChange")
    }


def get_pipeline_commit_id(pipeline_name):
    state = cp.get_pipeline_state(name=pipeline_name)

    for stage in state["stageStates"]:
        if stage["stageName"].lower() == "source":
            for action in stage.get("actionStates", []):
                exec = action.get("latestExecution", {})
                return exec.get("externalExecutionId")

    return None


def get_pipeline_source(pipeline_name):
    pipeline = cp.get_pipeline(name=pipeline_name)

    for stage in pipeline["pipeline"]["stages"]:
        if stage["name"].lower() == "source":
            action = stage["actions"][0]
            cfg = action["configuration"]
            return {
                "provider": action["actionTypeId"]["provider"],
                "repo": cfg.get("FullRepositoryId"),
                "branch": cfg.get("BranchName")
            }

    return {}


def get_pipeline_info(pipeline_name):
    status = get_pipeline_overall_status(pipeline_name)
    commit_id = get_pipeline_commit_id(pipeline_name)
    source = get_pipeline_source(pipeline_name)

    return {
        "pipeline": pipeline_name,
        **status,
        "commitId": commit_id,
        "source": source
    }
