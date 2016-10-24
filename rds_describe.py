#!/bin/env python
# coding: utf-8
import sys
import boto3
from boto3.session import Session

def rds_describe(profile):
    session = boto3.session.Session(profile_name=profile)
    client = session.client('rds')
    paginator = client.get_paginator('describe_db_instances')
    page_iterator = paginator.paginate()
    for page in page_iterator:
        for rds in page['DBInstances']:
            instance_name = rds['DBInstanceIdentifier']
            multi_az = rds['MultiAZ']
            instance_type = rds['DBInstanceClass']
            endpoint = rds['Endpoint']['Address']
            engine = rds['Engine']
            engine_ver = rds['EngineVersion']
            az = rds['AvailabilityZone']
            create_time = rds['InstanceCreateTime']
            print '{0: <20} MultiAZ:{1: <10}{2: <15}{3: <65}{4}{5: <15}{6: <20}{7}'.format(
                instance_name, multi_az, instance_type, endpoint,
                engine, engine_ver, az, create_time
            )

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 2):
        print 'example: python rds_describe.py [profile_name]'
        quit()
    profile = argvs[1]

    rds_describe(profile)
