import boto3
from datetime import datetime,timezone

iamclient = boto3.client("iam")

users = iamclient.list_users()['Users']

for user in users:

    keys = iamclient.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata']

    for key in keys:
        AccessKeyId = key['AccessKeyId']
        CreateDate = key['CreateDate']
        keyage = (datetime.now(timezone.utc)-CreateDate).days

        print(AccessKeyId,keyage)

# print(users)