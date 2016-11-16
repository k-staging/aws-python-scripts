#!/bin/env python
# coding: utf-8
import sys
import boto3
from boto3.session import Session
from datetime import datetime, timedelta


######################################################
# 取得したイベントログにフィルターを掛け、結果を出力
######################################################
def print_log(event_log):
    filter_messages = [
        'Finished recovery','Recovering cache',
        'scheduled for replacement','The replacement',
        'restarted','Failover'
    ]
    for filter_message in filter_messages:
        if filter_message in event_log['Message']:
            date = event_log['Date']
            source_identifier = event_log['SourceIdentifier']
            message = event_log['Message']
            print '{0: %Y-%m-%d-%H:%M} {1} {2}'.format(
                date, source_identifier, message
            )

#######################
# イベントログを取得
#######################
def elasticache_event_describe(profile):
    session = boto3.session.Session(profile_name = profile)
    client = session.client('elasticache')
    paginator = client.get_paginator('describe_events')
    now = datetime.now()
    two_weeks_ago = now - timedelta(days = 14)
    page_iterator = paginator.paginate(
        SourceType = 'cache-cluster',
        StartTime = two_weeks_ago,
        EndTime = now,
    )
    for page in page_iterator:
        for event_log in page['Events']:
            print_log(event_log)


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if argc != 2:
        print 'python elasticache_event_describe.py [profile]'
        quit()
    profile = argvs[1]

    elasticache_event_describe(profile)
