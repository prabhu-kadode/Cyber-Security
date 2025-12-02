import boto3

s3 = boto3.client('s3')
try:
    policies = s3.get_bucket_policy(Bucket="my-test-kadode")
    print(policies)
except Exception as e:
    print("no bucket polciy")

try:
    aclp = s3.get_bucket_acl(Bucket="my-test-kadode")
    print(aclp)
except Exception as e:
    print("No Acl So Far")

try:
    pap = s3.get_public_access_block(Bucket="my-test-kadode")
    print(pap)
except Exception as e:
    print("no public access polcies")