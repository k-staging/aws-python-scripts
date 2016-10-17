#!/bin/env python
# coding: utf-8
import sys
import boto3
from boto3.session import Session

def elasticache_list(profile):
    session = boto3.session.Session(profile_name=profile)
    elasticache = session.client('elasticache')
    elasticache = elasticache.describe_cache_clusters()
    elasticache = elasticache['CacheClusters']
    for elasticache in elasticache:
        print elasticache['CacheClusterId']

# main
if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    if (argc != 2):
        print 'example: python elasticache_describe.py [profile_name]'
        quit()

    profile = argvs[1]
    elasticache_list(profile)
