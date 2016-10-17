#!/bin/env python
# coding: utf-8
import sys
import boto3
from boto3.session import Session

def rds_describe(profile):
    session = boto3.session.Session(profile_name=profile)
    rds = session.client('rds')
    rds = rds.describe_db_instances()
    rds = rds['DBInstances']
    for rds in rds:
        print '{0} \t {1}'.format( rds['DBInstanceIdentifier'], rds['Endpoint']['Address'] )

# main
if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    if (argc != 2):
        print 'example: python rds_describe.py [profile_name]'
        quit()

    profile = argvs[1]
    rds_describe(profile)
