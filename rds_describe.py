#!/bin/env python
# coding: utf-8
import sys
import boto3
from boto3.session import Session

def describe(profile):
    rds_describe = []
    session = boto3.session.Session(profile_name=profile)
    client = session.client('rds')
    paginator = client.get_paginator('describe_db_instances')
    page_iterator = paginator.paginate()
    for page in page_iterator:
        for rds in page['DBInstances']:
            instance_name = rds['DBInstanceIdentifier']
            instance_type = rds['DBInstanceClass']
            endpoint = rds['Endpoint']['Address']
            engine = rds['Engine']
            engine_ver = rds['EngineVersion']
            az = rds['AvailabilityZone']
            create_time = rds['InstanceCreateTime']
            pg_name = ''
            for rds_pg in rds['DBParameterGroups']:
                pg_name = '{0} {1}'.format(pg_name, rds_pg['DBParameterGroupName'])
            describe = '{0: <30}  {1: <13} {2: <65} {3}{4: <7} {5: <11} {6: <13} {7: %Y-%m-%d-%H:%M}'.format(
                instance_name, instance_type, endpoint,
                engine, engine_ver, pg_name, az, create_time
            )
            if describe is not None:
                rds_describe.append(describe)
        return rds_describe

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 2):
        print 'example: python rds_describe.py [profile_name]'
        quit()
    profile = argvs[1]
    rds_describe = describe(profile)
    for rds_describe in rds_describe:
        print rds_describe
