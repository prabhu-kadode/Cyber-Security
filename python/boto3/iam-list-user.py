import boto3
iam = boto3.client("iam")

try:
    response = iam.list_users()
    
    for user in response['Users']:
        print(f"User: {user['UserName']}")
        print(f"UserId {user['UserId']}")
        mfa = iam.list_mfa_devices(UserName=user['UserName'])['MFADevices']
        access_keys = iam.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata']
        print("MFA Enabled" if mfa else "No MFA")
        print("Access key Metadata",access_keys)
except Exception as e:
    print(e)