#!/bin/env python
# coding: utf-8
import sys
import boto3

def describe(profile):
    kinesis_describe = []
    session = boto3.session.Session(profile_name=profile)
    client = session.client('kinesis')
    paginator = client.get_paginator('list_streams')
    page_iterator = paginator.paginate()
    for page in page_iterator:
        for kinesis in page['StreamNames']:
            describe = '{0:}'.format(
                kinesis
            )
            if describe is not None:
                kinesis_describe.append(describe)
        return kinesis_describe

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 2):
        print 'example: python kinesis_describe.py [profile_name]'
        quit()
    profile = argvs[1]
    kinesis_describe = describe(profile)
    for kinesis_describe in kinesis_describe:
        print kinesis_describe
