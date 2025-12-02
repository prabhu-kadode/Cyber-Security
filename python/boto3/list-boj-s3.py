import boto3

s3_client = boto3.client("s3")
params = {"Bucket":'my-test-kadode'}
paginator = s3_client.get_paginator("list_objects_v2")


for pages in paginator.paginate(**params):
    for obj in pages['Contents']:
        print(obj['Key'])




