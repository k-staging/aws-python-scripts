#!/bin/env python
# coding: utf-8
import sys
import boto3
from boto3.session import Session

def describe(profile, keyword):
    ec2_describe = []
    session = boto3.session.Session(profile_name=profile)
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
                        instance_nametag = nametag['Value'].encode('utf-8')
                instance_id = ec2['InstanceId']
                state = ec2['State']['Name']
                instance_type = ec2['InstanceType']
                public_dns = ec2['PublicDnsName']
                private_ip = ''
                if 'PrivateIpAddress' in ec2:
                    private_ip = ec2['PrivateIpAddress']
                az = ec2['Placement']['AvailabilityZone']
                key_pair = ec2['KeyName']
                launchtime = ec2['LaunchTime']
                describe = '{0: <20} {1: <20} {2: <10} {3: <10} {4: <57} {5: <15} {6: <20} {7: <10} {8: %Y-%m-%d-%H:%M}'.format(
                    instance_nametag, instance_id, state, instance_type,
                    public_dns, private_ip, az, key_pair, launchtime
                )
                if describe is not None:
                    ec2_describe.append(describe)
        return ec2_describe

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
    ec2_describe = describe(profile, keyword)
    for ec2_describe in ec2_describe:
        print ec2_describe
