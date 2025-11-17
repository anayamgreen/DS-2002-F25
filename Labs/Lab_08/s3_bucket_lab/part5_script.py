import boto3
import sys

def upload_and_presign(local_file, bucket, expiration):
    s3 = boto3.client('s3', region_name='us-east-1')

    s3.upload_file(local_file, bucket, local_file)

    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': local_file},
        ExpiresIn=expiration
    )
    return url

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <local_file> <bucket> <expiration_seconds>")
        sys.exit(1)

    local_file = sys.argv[1]
    bucket = sys.argv[2]
    expiration = int(sys.argv[3])

    url = upload_and_presign(local_file, bucket, expiration)
    print("Presigned URL:", url)

