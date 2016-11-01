#!/bin/env python
# coding: utf-8
import sys
import boto3
from boto3.session import Session

def s3_describe(profile):
    session = boto3.session.Session(profile_name = profile)
    client = session.client('s3')
    s3 = client.list_buckets()
    for s3 in s3['Buckets']:
        bucket_name = s3['Name']
        create_time = s3['CreationDate']
        print '{0: <50}  {1: %Y-%m-%d-%H:%M}'.format(
            bucket_name, create_time
        )

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 2):
        print 'example: python s3_describe.py [profile_name]'
        quit()
    profile = argvs[1]

    s3_describe(profile)
