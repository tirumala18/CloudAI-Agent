import boto3
import json
from langchain.tools import tool
from app.aws_client import get_boto_client


# ─────────────────────────────────────────────
# S3
# ─────────────────────────────────────────────
@tool
def list_s3_buckets(query: str = "") -> str:
    """List all S3 buckets in the AWS account."""
    try:
        s3 = get_boto_client("s3")
        response = s3.list_buckets()
        buckets = [b["Name"] for b in response.get("Buckets", [])]
        return f"S3 Buckets ({len(buckets)} total):\n" + "\n".join(f"  - {b}" for b in buckets)
    except Exception as e:
        return f"Error listing S3 buckets: {str(e)}"


# ─────────────────────────────────────────────
# EC2
# ─────────────────────────────────────────────
@tool
def describe_ec2_instances(filter_by: str = "") -> str:
    """
    List EC2 instances with their state, type, and name tag.
    Optionally filter by instance name or state (e.g. 'running').
    """
    try:
        ec2 = get_boto_client("ec2")
        response = ec2.describe_instances()
        instances = []

        for reservation in response["Reservations"]:
            for inst in reservation["Instances"]:
                name = next(
                    (t["Value"] for t in inst.get("Tags", []) if t["Key"] == "Name"),
                    "unnamed"
                )
                state = inst["State"]["Name"]
                itype = inst["InstanceType"]
                iid = inst["InstanceId"]

                if filter_by and filter_by.lower() not in name.lower() and filter_by.lower() != state:
                    continue

                instances.append(f"  - {name} | {iid} | {itype} | {state}")

        if not instances:
            return "No EC2 instances found."
        return f"EC2 Instances:\n" + "\n".join(instances)
    except Exception as e:
        return f"Error describing EC2 instances: {str(e)}"


# ─────────────────────────────────────────────
# ECS
# ─────────────────────────────────────────────
@tool
def get_ecs_service_status(cluster_and_service: str) -> str:
    """
    Get ECS service deployment status.
    Input format: 'cluster-name/service-name' or just 'service-name'.
    Example: 'payments-cluster/payments-service' or 'payments-service'
    """
    try:
        parts = cluster_and_service.strip().split("/")
        if len(parts) == 2:
            cluster, service = parts[0], parts[1]
        else:
            cluster = "default"
            service = parts[0]

        ecs = get_boto_client("ecs")
        response = ecs.describe_services(cluster=cluster, services=[service])
        services = response.get("services", [])

        if not services:
            return f"No ECS service found: {service} in cluster {cluster}"

        svc = services[0]
        return (
            f"ECS Service: {svc['serviceName']}\n"
            f"  Cluster:  {cluster}\n"
            f"  Status:   {svc['status']}\n"
            f"  Desired:  {svc['desiredCount']}\n"
            f"  Running:  {svc['runningCount']}\n"
            f"  Pending:  {svc['pendingCount']}\n"
            f"  Task Def: {svc['taskDefinition'].split('/')[-1]}"
        )
    except Exception as e:
        return f"Error fetching ECS service status: {str(e)}"


# ─────────────────────────────────────────────
# EKS
# ─────────────────────────────────────────────
@tool
def list_eks_clusters(query: str = "") -> str:
    """List all EKS clusters in the AWS account."""
    try:
        eks = get_boto_client("eks")
        response = eks.list_clusters()
        clusters = response.get("clusters", [])
        if not clusters:
            return "No EKS clusters found."
        return "EKS Clusters:\n" + "\n".join(f"  - {c}" for c in clusters)
    except Exception as e:
        return f"Error listing EKS clusters: {str(e)}"


@tool
def describe_eks_cluster(cluster_name: str) -> str:
    """
    Get detailed status of an EKS cluster by name.
    Example input: 'payments-cluster'
    """
    try:
        eks = get_boto_client("eks")
        r = eks.describe_cluster(name=cluster_name)
        c = r["cluster"]
        return (
            f"EKS Cluster: {c['name']}\n"
            f"  Status:     {c['status']}\n"
            f"  Version:    {c['version']}\n"
            f"  Endpoint:   {c.get('endpoint', 'N/A')}\n"
            f"  Region:     {c['arn'].split(':')[3]}"
        )
    except Exception as e:
        return f"Error describing EKS cluster: {str(e)}"
