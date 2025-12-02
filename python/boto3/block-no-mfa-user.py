import boto3

def block_no_mfm_user(func):
    def wrapper(*args,**kwargs):
        iam = boto3.client("iam")
        sts = boto3.client('sts')
        ident=  sts.get_caller_identity()
        arn = ident['Arn']
        user = arn.split('/')[-1]
        mfa = iam.list_mfa_devices(UserName=user)['MFADevices']
        if not mfa:
            print("No MFA enabled for this user",user)
            print("Access Denied...")
            return
        print("Access granted for below user")
        print("Arn:",arn)
        return func(*args,**kwargs)
    return wrapper
@block_no_mfm_user
def list_buckets():
    s3=boto3.client('s3')
    for bucket in s3.buckets.all():
        print(bucket)

list_buckets()

        
            