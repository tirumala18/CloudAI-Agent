import boto3

def list_s3():
    s3 = boto3.client("s3")
    return s3.list_buckets()
def describe_ec2():
    ec2 = boto3.client("ec2")
    return ec2.describe_instances()
