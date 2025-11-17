#!/bin/bash
set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <expiration_seconds>"
    exit 1
fi

EXPIRATION=$1
IMAGE_FILE="nami_image.png"
BUCKET="ds2002-f25-yfx3ds"

aws s3 cp "$IMAGE_FILE" "s3://$BUCKET/$IMAGE_FILE" --acl private

PRESIGNED_URL=$(aws s3 presign "s3://$BUCKET/$IMAGE_FILE" --expires-in "$EXPIRATION")

echo "Presigned URL for $IMAGE_FILE (expires in $EXPIRATION seconds):"
echo "$PRESIGNED_URL"

