import boto3
import argparse
from botocore.exceptions import ClientError, NoCredentialsError

class S3Sentinel:

    def __init__(self, profile=None, region=None):
        # Initialize the scanner with optional AWS profile and region
        self.session = boto3.Session(profile_name=profile, region_name=region)
        self.s3 = self.session.resource('s3')

    def get_buckets(self):
        # Retrieve all S3 buckets in the account
        return list(self.s3.buckets.all())

    def check_bucket_encryption(self, bucket):
        # Even though encryption is enabled by default you can disable it(No idea why you would)
        try:
            s3_client = self.session.client('s3')
            response = s3_client.get_bucket_encryption(Bucket=bucket.name)
            rules = response['ServerSideEncryptionConfiguration']['Rules']
            return f"Encryption enabled - {rules}"
        except ClientError as e:
            if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                return "Encryption not configured"
            else:
                return f"Error checking encryption: {str(e)}"

    def check_versioning(self, bucket):
        # Check if versioning is enabled for the bucket
        versioning = bucket.Versioning()
        if (versioning.status == 'enabled'):
            return "Versioning enabled"
        else:
            return "Versioning disabled"

    def check_public_access_block(self, bucket):
        # Check the public access block settings for the bucket
        try:
            s3_client = self.session.client('s3')
            response = s3_client.get_public_access_block(Bucket=bucket.name)
            config = response['PublicAccessBlockConfiguration']
            return f"Public access block configuration - {config}"
        except ClientError as error:
            if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
                return "Public access block not configured"
            else:
                return f"Error checking public access block: {str(error)}"

    def check_logging(self, bucket):
        # Check if server access logging is enabled for the bucket
        try:
            logging = bucket.Logging().logging_enabled
            if(logging):
                return "Logging enabled"
            else:
                return "Logging disabled"
        except ClientError:
            return "Unable to retrieve logging information"

    def check_lifecycle(self, bucket):
        # Check if any lifecycle rules are configured for the bucket
        try:
            lifecycle = bucket.Lifecycle().rules
            return f"Lifecycle rules configured - {len(lifecycle)} rules"
        except ClientError:
            return "No lifecycle rules configured"

    def check_acl(self, bucket):
        # Check the ACL permissions of the bucket
        try:
            acl = bucket.Acl()
            issues = []
            for grant in acl.grants:
                grantee = grant.get('Grantee', {})
                uri = grantee.get('URI', '')
                permissions = grant.get('Permission', '')
                # Check for potentially risky permissions granted to all users or authenticated users
                if uri in ['http://acs.amazonaws.com/groups/global/AuthenticatedUsers', 'http://acs.amazonaws.com/groups/global/AllUsers']:
                    group_type = "Authenticated Users" if "AuthenticatedUsers" in uri else "All Users"
                    issues.append(f"Grants {permissions} permissions to all {group_type} globally")
            return issues if issues else "No concerning ACL permissions found"
        except ClientError as error:
            return f"Couldn't get ACL. Error: {error}"

    def scan_bucket(self, bucket):
        # Perform all checks on a single bucket and print results
        print(f"\nScanning bucket: {bucket.name}")
        print(f"Encryption: {self.check_bucket_encryption(bucket)}")
        print(f"Versioning: {self.check_versioning(bucket)}")
        print(f"Public Access Block: {self.check_public_access_block(bucket)}")
        print(f"Logging: {self.check_logging(bucket)}")
        print(f"Lifecycle: {self.check_lifecycle(bucket)}")
        print(f"ACL: {self.check_acl(bucket)}")

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="S3 Sentinel")
    parser.add_argument("--profile", help="AWS profile name")
    parser.add_argument("--region", help="AWS region")
    args = parser.parse_args()

    try:
        # Initialize the scanner with provided profile and region (if any)
        scanner = S3Sentinel(profile=args.profile, region=args.region)
        buckets = scanner.get_buckets()

        print(f"Found {len(buckets)} buckets.")
        # Ask user if they want to scan all buckets or select specific ones
        scan_all = input("Do you want to scan all buckets? (y/n): ").lower() == 'y'

        if scan_all:
            # Scan all buckets if user chose to do so
            for bucket in buckets:
                scanner.scan_bucket(bucket)
        else:
            # Allow user to select specific buckets to scan
            while True:
                bucket_name = input("Enter the name of the bucket to scan (or 'q' to quit): ")
                if bucket_name.lower() == 'q':
                    break
                bucket = next((b for b in buckets if b.name == bucket_name), None)
                if bucket:
                    scanner.scan_bucket(bucket)
                else:
                    print(f"Bucket '{bucket_name}' not found.")

    except NoCredentialsError:
        # Handle case where AWS credentials are not found
        print("No AWS credentials found. Please configure your AWS credentials.")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()