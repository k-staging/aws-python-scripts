#!/bin/env python
# coding: utf-8
from __future__ import print_function
import sys
from boto3.session import Session


class GetParameter:
    def __init__(self, *args):
        self.args = args[0]

    def check_parameter(self):
        profile = ''
        keyword = ''
        if len(self.args) == 2 or len(self.args) == 3:
            profile = self.args[1]
        if len(self.args) == 3:
            keyword = self.args[2]

        return profile, keyword


class GetSession:
    def __init__(self, profile):
        self.profile = profile

    def get_session(self):
        session = Session(profile_name=self.profile)
        return session.client('ec2')


class DescribeInstances:
    def __init__(self, client, keyword):
        self.client = client
        self.keyword = keyword

    def get_instances(self):
        ec2_list = []
        get_ec2 = self.client.describe_instances(
            Filters=[
                {
                    'Name': 'tag-value',
                    'Values': [
                        '{0}{1}{0}'.format("*", self.keyword),
                    ]
                }
            ]
        )
        for ec2_instances in get_ec2['Reservations']:
            for ec2 in ec2_instances['Instances']:
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
                describe = '{0:<20} {1:<20} {2:<10} {3:<10} {4:<57} {5:<15} {6:<20} {7:<10} {8:%Y-%m-%d-%H:%M}'.format(
                    instance_nametag, instance_id, state, instance_type,
                    public_dns, private_ip, az, key_pair, launchtime
                )
                if describe is not None:
                    ec2_list.append(describe)
        return ec2_list


if __name__ == '__main__':
    parameter = GetParameter(sys.argv)
    profile, keyword = parameter.check_parameter()
    session = GetSession(profile)
    client = session.get_session()
    ec2 = DescribeInstances(client, keyword)
    ec2_instances = ec2.get_instances()

    for ec2 in ec2_instances:
        print(ec2)
