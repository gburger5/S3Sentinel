import boto3
from botocore.exceptions import ClientError

def get_buckets():
    # Gets all Available S3 Buckets
    buckets = []
    s3_resource = boto3.resource("s3")
    for bucket in s3_resource.buckets.all():
        buckets.append(bucket)
    return buckets

"""def get_bucket_policy(buckets):
    bucket_policy_list = []
    for bucket in buckets:
        bucket_name = bucket.name
        try:
            bucket_policy = bucket.get_bucket_policy(Bucket=bucket_name)
            bucket_policy_list.append({
                'Statement' : bucket_policy.statement,
                ''
            })"""



def get_acl(buckets):
    # Gets ACL Policy for each Bucket and makes it Readable
    acl_list = []
    for bucket in buckets: 
        try: 
            acl = bucket.acl()
            acl_list.append({                      
                'Bucket': bucket.name,
                'Grants': acl.grants
            })
        except ClientError as error:
            print(f"Couldn't Get ACL For {bucket.name}. Error: {error}")
    return acl_list

def check_grants(grants, acl_list):
    # Logic for Checking ACL Grants for Invalid Permissions
    bucket_name = acl_list['Bucket']
    grantee = grants['Grantee']
    uri = grantee['uri']
    permissions = grants['Permission']
    # Global Auth Users + Faulty Permissions Checks
    if uri == 'http://acs.amazonaws.com/groups/global/AuthenticatedUsers' and permissions == 'FULL_CONTROL':
        print(f"{bucket_name} grants FULL_CONTROL permissions to all Authenticated Users globally.")
    elif uri == 'http://acs.amazonaws.com/groups/global/AuthenticatedUsers' and permissions == 'READ':
        print(f"{bucket_name} grants READ permissions to all Authenticated Users globally.")
    elif uri == 'http://acs.amazonaws.com/groups/global/AuthenticatedUsers' and permissions == 'READ_ACP':
        print(f"{bucket_name} grants READ_ACP permissions to all Authenticated Users globally.")
    # Global All Users + Faulty Permissions Checks
    elif uri == 'http://acs.amazonaws.com/groups/global/AllUsers' and permissions == 'FULL_CONTROL':
        print(f"{bucket_name} grants FULL_CONTROL permissions to All Users globally.")
    elif uri == 'http://acs.amazonaws.com/groups/global/AllUsers' and permissions == 'READ':
        print(f"{bucket_name} grants READ permissions to All Users globally.")
    elif 'http://acs.amazonaws.com/groups/global/AllUsers' and permissions == 'READ_ACP':
        print(f"{bucket_name} grants READ_ACP permissions to All Users globally.")

def check_acl(acl_list):
    # Command run for ACL Checking
    for bucket in acl_list: 
        grants = acl_list['Grants']
        check_grants(grants, acl_list)


    

    



