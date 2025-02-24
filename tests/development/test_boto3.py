import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# Create S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="us-east-2",  # specify your region
)

try:
    # List buckets to test connectivity
    response = s3.list_buckets()
    print("Buckets:")
    for bucket in response["Buckets"]:
        print(f"- {bucket['Name']}")
    print("Credentials are valid!")
except Exception as e:
    print(f"Error testing credentials: {e}")
