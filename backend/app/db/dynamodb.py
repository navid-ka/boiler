import boto3
from botocore.exceptions import ClientError
import logging

def get_dynamodb():
    resource = boto3.resource(
        "dynamodb",
        region_name="us-east-1",
        endpoint_url="http://dynamodb:8000",
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy",
    )
    return resource

def get_items_table():
    dynamodb = get_dynamodb()
    return dynamodb.Table("Items")