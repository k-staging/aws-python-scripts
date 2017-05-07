#!/bin/env python
# coding: utf-8
import sys
import boto3


def describe(profile, key_word):
    session = boto3.session.Session(profile_name=profile)
    client = session.client('route53')
    hosted_zones = client.list_hosted_zones()
    for hosted_zone in hosted_zones['HostedZones']:
        if key_word == '' or key_word in hosted_zone.values():
            hosted_zone_name = hosted_zone['Name']
            hosted_zone_id = hosted_zone['Id']
            private_zone = hosted_zone['Config']['PrivateZone']
            print '{0: <30}{1: <30} private_zone:{2}'.format(
                hosted_zone_name, hosted_zone_id,
                private_zone
            )


if __name__ == '__main__':
    key_word = ''
    argvs = sys.argv
    argc = len(argvs)
    if argc <= 2 and argc >= 3:
        print 'python route53_describe_hosted_zone.py [profile]'
        quit()
    if argc == 3:
        key_word = argvs[2]
    profile = argvs[1]

    route53_describe = describe(profile, key_word)
