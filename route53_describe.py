#!/bin/env python
# coding: utf-8
import sys
import boto3
from boto3.session import Session

def route53_describe(profile):
    session = boto3.session.Session(profile_name = profile)
    client = session.client('route53')
    paginator = client.get_paginator('list_hosted_zones')
    page_iterator = paginator.paginate()
    for page in page_iterator:
        for hosted_zone in page['HostedZones']:
            hosted_zone_name = hosted_zone['Name']
            hosted_zone_id = hosted_zone['Id']
            paginator = client.get_paginator('list_resource_record_sets')
            page_iterator = paginator.paginate(HostedZoneId = hosted_zone_id)
            for page in page_iterator:
                for records in page['ResourceRecordSets']:
                    ttl = ''
                    resorce_record = ''
                    record_name = records['Name']
                    record_type = records['Type']
                    if 'TTL' in records:
                        ttl = records['TTL']
                    if 'ResourceRecords' in records:
                        for records in records['ResourceRecords']:
                            resorce_record = '{0} {1}'.format(resorce_record, records['Value'])
                        print '{0: <60} {1: <9} {2: <9} {3: <15}'.format(
                            record_name, ttl, record_type, resorce_record
                        )
                    if 'AliasTarget' in records:
                        alias_target = records['AliasTarget']['DNSName']
                        print '{0: <60} {1: <9} {2: <9}  {3: <15}'.format(
                            record_name, ttl, record_type, alias_target
                        )

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if argc != 2:
        print 'python ec2_describe.py [profile]'
        quit()
    profile = argvs[1]

    route53_describe(profile)
