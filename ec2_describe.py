#!/bin/env python
# coding: utf-8
import sys
import boto3
from boto3.session import Session

def ec2_describe(profile):
    session = boto3.session.Session(profile_name=profile)
    ec2_list = session.client('ec2')
    ec2_list = ec2_list.describe_instances()
    ec2_list = ec2_list['Reservations']
    for ec2 in ec2_list:
        instance_id = ec2['Instances'][0]['InstanceId']
        publicdns_name = ec2['Instances'][0]['PublicDnsName']
        instance_launchtime = ec2['Instances'][0]['LaunchTime']
        instance_type = ec2['Instances'][0]['InstanceType']
        instance_nametag = ec2['Instances'][0]['Tags']
        print '{0} \t {1} \t {2} \t {3}'.format( instance_id, instance_type, instance_launchtime, publicdns_name )

# main
if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    if (argc != 2):
        print 'example: python ec2_describe.py [profile_name]'
        quit()

    profile = argvs[1]
    ec2_describe(profile)
