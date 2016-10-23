#!/bin/env python
# coding: utf-8
import sys
import boto3
from boto3.session import Session

def ec2_describe(profile, keyword):
    session = boto3.session.Session(profile_name = profile)
    client = session.client('ec2')
    paginator = client.get_paginator('describe_instances')
    page_iterator = paginator.paginate(
        Filters=[
            {
                'Name': 'tag-value',
                'Values': [
                    '{0}{1}{0}'.format("*", keyword),
                ]
            }
        ]
    )
    for page in page_iterator:
        for ec2_list in page['Reservations']:
            for ec2 in ec2_list['Instances']:
                for nametag in ec2['Tags']:
                    if nametag['Key'] == 'Name':
                        instance_nametag = nametag['Value']
                instance_id = ec2['InstanceId']
                public_dns = ec2['PublicDnsName']
                private_ip = ec2['PrivateIpAddress']
                instance_type = ec2['InstanceType']
                instance_launchtime = ec2['LaunchTime']
                az = ec2['Placement']['AvailabilityZone']
                print '{0: <40}{1: <15}{2: <15}{3: <60}{4: <15}{5: <20}{6}'.format(
                    instance_nametag, instance_id, instance_type,
                    public_dns, private_ip, az, instance_launchtime
                )

if __name__ == '__main__':
    keyword = ''
    argvs = sys.argv
    argc = len(argvs)
    if argc != 2 and argc != 3:
        print 'python ec2_describe.py [profile] {nametag]'
        quit()
    if argc == 3:
        keyword = argvs[2]

    profile = argvs[1]
    ec2_describe(profile, keyword)
