import boto3
class Secure_boto:
    def client(self,service,**kwargs):
        if self.is_MFA_Eanbled():
            return boto3.client(service,**kwargs)
        print("MFA Not Enabled,Access denied")
        raise PermissionError(
                "❌ Access Denied: MFA not enabled for this IAM user."
            )
    def resource(self,service,**kwargs):
        if self.is_MFA_Eanbled():
            return boto3.resource(service,**kwargs)
        print("MFA Not Enabled,Access denied")
        raise PermissionError(
                "❌ Access Denied: MFA not enabled for this IAM user."
            )

    def is_MFA_Eanbled(self):
        return False

securebotot = Secure_boto()
s3_client = securebotot.resource("s3")
for bucket in s3_client.buckets.all():
    print(bucket.name)


