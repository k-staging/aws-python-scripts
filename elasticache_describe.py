#!/bin/env python
# coding: utf-8
import sys
import boto3
from boto3.session import Session

def elasticache_describe(profile):
    session = boto3.session.Session(profile_name=profile)
    client = session.client('elasticache')
    paginator = client.get_paginator('describe_cache_clusters')
    page_iterator = paginator.paginate(ShowCacheNodeInfo = True)
    for page in page_iterator:
        for elasticache in page['CacheClusters']:
            clusterid = elasticache['CacheClusterId']
            replicaid = ''
            if 'ReplicationGroupId' in elasticache:
                replicaid = elasticache['ReplicationGroupId']
            instance_type = elasticache['CacheNodeType']
            engine = elasticache['Engine']
            engine_ver = elasticache['EngineVersion']
            maintenance_window= elasticache['PreferredMaintenanceWindow']
            for elasticache in elasticache['CacheNodes']:
                endpoint = elasticache['Endpoint']['Address']
                az = elasticache['CustomerAvailabilityZone']
                create_time = elasticache['CacheNodeCreateTime']
                print '{0: <20} {1: <17} {2: <60} {3}{4: <7} {5: <12} {6: %Y-%m-%d-%H:%M}  {7}'.format(
                    clusterid, instance_type, endpoint, engine,
                    engine_ver, az, create_time, replicaid
                )

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if argc != 2:
        print 'python ec2_describe.py [profile]'
        quit()

    profile = argvs[1]
    elasticache_describe(profile)
