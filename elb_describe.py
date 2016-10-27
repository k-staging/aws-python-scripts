#!/bin/env python
# coding: utf-8
import sys
import boto3
from boto3.session import Session

def elb_describe(profile):
    session = boto3.session.Session(profile_name=profile)
    client = session.client('elb')
    paginator = client.get_paginator('describe_load_balancers')
    page_iterator = paginator.paginate()
    for page in page_iterator:
        for elb in page['LoadBalancerDescriptions']:
            elb_name = elb['LoadBalancerName']
            scheme = elb['Scheme']
            dns_name = elb['DNSName']
            create_time = elb['CreatedTime']
            listener = ''
            for elb_listener in elb['ListenerDescriptions']:
                instance_port = elb_listener['Listener']['InstancePort']
                elb_port = elb_listener['Listener']['LoadBalancerPort']
                listener = '{0} {1} to {2}.'.format(listener, elb_port, instance_port)
            print '{0: <30} {1: <17} {2: <75} {3: %Y-%m-%d-%H:%M}  {4}'.format(elb_name, scheme, dns_name, create_time, listener)

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    if (argc != 2):
        print 'python elb_describe.py [profile]'
        quit()

    profile = argvs[1]
    elb_describe(profile)
