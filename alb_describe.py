#!/bin/env python
# coding: utf-8
import sys
import boto3
from boto3.session import Session

def alb_describe(profile):
    session = boto3.session.Session(profile_name=profile)
    alb = session.client('elbv2')
    alb = alb.describe_load_balancers()
    alb = alb['LoadBalancers']
    for alb in alb:
        alb_arn = alb['LoadBalancerArn'].replace("/"," ")
        alb_arn = alb_arn.split(' ')
        alb_dnsname = alb['DNSName']
        print '{0}/{1} \t {2}'.format( alb_arn[-2], alb_arn[-1], alb_dnsname )

# main
if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    if (argc != 2):
        print 'example: python alb_describe.py [profile_name]'
        quit()

    profile = argvs[1]
    alb_describe(profile)
