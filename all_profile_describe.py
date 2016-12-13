#!/bin/env python
# coding: utf-8
import os
import sys
import boto3
from boto3.session import Session
import ConfigParser

config = ConfigParser.SafeConfigParser()
config.read(os.environ.get('AWS_CONFIG_FILE'))
profiles = config.sections()

def describe(script, keyword):
    for profile in profiles:
        describe = ''
        module = __import__(script)
        if 'ec2_describe' != module.__name__:
            profile_describe = module.describe(profile)
        else:
            profile_describe = module.describe(profile, keyword)
        if profile_describe is not None and len(profile_describe) != 0:
            for tmp_describe in profile_describe:
                describe = '{0}{1}\n'.format(describe, tmp_describe)
            print '[{0} {1}]\n{2}'.format(
                profile, script, describe
            )

if __name__ == '__main__':
    keyword = ''
    argvs = sys.argv
    argc = len(argvs)
    if argc != 2 and argc != 3:
        print 'example: python all_account_describe.py [script]'
        quit()
    if argc == 3:
        keyword = argvs[2]
    script = argvs[1].replace('.py','')
    describe(script, keyword)
