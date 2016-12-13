#!/usr/local/bin/python
# coding: utf-8
import sys
import boto3
from boto3.session import Session

def ec2_list(client, instance_id):
    paginator = client.get_paginator('describe_instances')
    page_iterator = paginator.paginate(
        Filters=[
            {
                'Name': 'instance-id',
                'Values': [
                    instance_id,
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
    return instance_nametag


def describe(profile):
    ec2_event = []
    session = boto3.session.Session(profile_name=profile)
    client = session.client('ec2')
    paginator = client.get_paginator('describe_instance_status')
    page_iterator = paginator.paginate(
        Filters=[
            {
                'Name': 'event.code',
                'Values': [
                    'instance-reboot', 'system-reboot', 'system-maintenance',
                    'instance-retirement', 'instance-stop'
                ]
            },
        ],
    )
    for page in page_iterator:
        for ec2_eventlog in page['InstanceStatuses']:
            instance_id = ec2_eventlog['InstanceId']
            instance_nametag = ec2_list(client, instance_id)
            for ec2_eventlog in ec2_eventlog['Events']:
                event_type = ec2_eventlog['Code']
                description = ec2_eventlog['Description']
                start_time = ec2_eventlog['NotBefore']
            tmp_event ='Name: {0}\nInstanceID: {1}\nEventType: {2}\nDescription: {3}\nStartTime: {4}'.format(
                instance_nametag, instance_id, event_type,
                description, start_time.strftime('%Y-%m-%d %H:%M:%S')
            )
            ec2_event.append(tmp_event)
    return ec2_event

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if argc != 2:
        print 'python ec2_event_describe.py [profile]'
        quit()
    profile = argvs[1]
    ec2_event = describe(profile)
    for ec2_event in ec2_event:
        print ec2_event
