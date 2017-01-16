#!/bin/env python
# coding: utf-8
import sys
import boto3

def describe(profile):
    iam_user_describe = []
    session = boto3.session.Session(profile_name=profile)
    client = session.client('iam')
    paginator = client.get_paginator('list_users')
    page_iterator = paginator.paginate()
    for page in page_iterator:
        for iam_user in page['Users']:
            last_used = ''
            iam_user_name = iam_user['UserName']
            iam_user_arn = iam_user['Arn']
            if 'PasswordLastUsed' in iam_user:
                last_used = iam_user['PasswordLastUsed']
            describe = '{0: <30} {1: <60} {2}'.format(
                iam_user_name, iam_user_arn, last_used
            )
            if describe is not None:
                iam_user_describe.append(describe)
        return iam_user_describe

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 2):
        print 'example: python iam_user_describe.py [profile_name]'
        quit()
    profile = argvs[1]
    iam_user_describe = describe(profile)
    for iam_user_describe in iam_user_describe:
        print iam_user_describe
