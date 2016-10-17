#!/bin/env python
# coding: utf-8
import sys
import boto3
from boto3.session import Session

def elb_describe(profile):
    session = boto3.session.Session(profile_name=profile)
    elb = session.client('elb')
    elb = elb.describe_load_balancers()
    elb = elb['LoadBalancerDescriptions']
    for elb in elb:
        print '{0} \t {1}'.format( elb['LoadBalancerName'], elb['DNSName'] )

# main
if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    if (argc != 2):
        print 'example: python elb_describe.py [profile_name]'
        quit()

    profile = argvs[1]
    elb_describe(profile)
