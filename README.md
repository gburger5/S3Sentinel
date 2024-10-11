# S3 Sentinel

S3 Sentinel is a Python-based tool designed to scan and analyze the security configuration of Amazon S3 buckets. It helps identify potential security risks and misconfigurations in your S3 buckets, allowing you to maintain better security practices for your cloud storage.

## Features

S3 Sentinel checks the following security aspects of S3 buckets:

- Encryption status
- Versioning configuration
- Public access block settings
- Logging configuration
- Lifecycle rules
- ACL permissions

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher
- AWS CLI configured with appropriate credentials
- `boto3` library installed

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/s3-sentinel.git
   cd s3-sentinel
   ```

2. Install the required Python packages:
   ```
   pip install boto3
   ```

3. Ensure your AWS credentials are properly configured. You can do this by running:
   ```
   aws configure
   ```

## Usage

To use S3 Sentinel, follow these steps:

1. Run the script:
   ```
   python s3Sentinel.py [--profile PROFILE_NAME] [--region REGION_NAME]
   ```

   - `--profile`: (Optional) Specify an AWS profile to use
   - `--region`: (Optional) Specify an AWS region to scan

2. The script will prompt you to choose between scanning all buckets or selecting specific ones.

3. Review the output for each scanned bucket, which will include information about:
   - Encryption status
   - Versioning configuration
   - Public access block settings
   - Logging configuration
   - Lifecycle rules
   - ACL permissions

## Example Output

```
Scanning bucket: my-example-bucket
Encryption: Encryption enabled - {'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}]}
Versioning: Versioning enabled
Public Access Block: Public access block configuration - {'BlockPublicAcls': True, 'IgnorePublicAcls': True, 'BlockPublicPolicy': True, 'RestrictPublicBuckets': True}
Logging: Logging disabled
Lifecycle: No lifecycle rules configured
ACL: No concerning ACL permissions found
```

## Contributing

Contributions to S3 Sentinel are welcome. Please feel free to submit a Pull Request.

## Disclaimer

S3 Sentinel is a tool to assist in identifying potential security risks in S3 buckets. It does not guarantee complete security and should be used as part of a comprehensive security strategy. Always follow AWS best practices and consult with security professionals when dealing with sensitive data.
