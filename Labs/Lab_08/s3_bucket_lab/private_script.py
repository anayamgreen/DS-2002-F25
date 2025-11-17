import boto3
import sys
import os

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 private_fscript.py <local_file> <bucket_name>")
        sys.exit(1)

    local_file = sys.argv[1]
    bucket = sys.argv[2]
    s3_key = os.path.basename(local_file)

    if not os.path.isfile(local_file):
        print(f"Error: File '{local_file}' does not exist.")
        sys.exit(1)

    s3 = boto3.client('s3', region_name="us-east-1")

    s3.upload_file(
        Filename=local_file,
        Bucket=bucket,
        Key=s3_key
    )

    print("\nUpload completed successfully!")
    print(f"File uploaded to: s3://{bucket}/{s3_key}")
    print("\nTry accessing it in the browser. You SHOULD get:")
    print("'AccessDenied' because the object is PRIVATE.")

if __name__ == "__main__":
    main()

