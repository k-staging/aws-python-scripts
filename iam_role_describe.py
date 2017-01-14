#!/bin/env python
# coding: utf-8
import sys
import boto3

def describe(profile):
    iam_role_describe = []
    session = boto3.session.Session(profile_name=profile)
    client = session.client('iam')
    paginator = client.get_paginator('list_roles')
    page_iterator = paginator.paginate()
    for page in page_iterator:
        for iam_role in page['Roles']:
            iam_role_name = iam_role['RoleName']
            iam_role_arn = iam_role['Arn']
            describe = '{0: <20} {1}'.format(
                iam_role_name, iam_role_arn
            )
            if describe is not None:
                iam_role_describe.append(describe)
        return iam_role_describe

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 2):
        print 'example: python iam_role_describe.py [profile_name]'
        quit()
    profile = argvs[1]
    iam_role_describe = describe(profile)
    for iam_role_describe in iam_role_describe:
        print iam_role_describe
