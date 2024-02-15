#!/usr/bin/python

import os
import boto3
import argparse


parser = argparse.ArgumentParser(description='upload folder to aws s3 bucket')
parser.add_argument('--source', required=True, type=str, help="source directory")
parser.add_argument('--bucket', required=True, type=str, help="target s3 bucket name")
parser.add_argument('--destination', required=True, type=str, help="destination directory")
parser.add_argument('--awsRegion', required=True, type=str, help="target aws region")
parser.add_argument('--awsAccessKeyID', required=True, type=str, help="AWS access key id, get it from IAM users")
parser.add_argument('--awsSecretAccessKey', required=True, type=str, help="AWS secret access key, get it from IAM users")
args = parser.parse_args()

source = args.source
bucket = args.bucket
destination = args.destination
aws_region = args.awsRegion
aws_access_key_id = args.awsAccessKeyID
aws_secret_access_key = args.awsSecretAccessKey

client = boto3.client('s3', region_name = aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

for root, dirs, files in os.walk(source):
    for filename in files:
        local_path = os.path.join(root, filename)
        relative_path = os.path.relpath(local_path, source)
        s3_path = os.path.join(destination, relative_path)
        print('Searching "%s" in "%s"' % (s3_path, bucket))
        try:
            client.head_object(Bucket=bucket, Key=s3_path)
            print ("Path found on S3! Skipping %s..." % s3_path)
        except:
            print("Uploading %s..." % s3_path)
            client.upload_file(local_path, bucket, s3_path)

