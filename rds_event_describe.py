#!/bin/env python
# coding: utf-8
import sys
import boto3
from boto3.session import Session
from datetime import datetime, timedelta

def rds_event_describe(profile):
    session = boto3.session.Session(profile_name = profile)
    client = session.client('rds')
    #################################
    # RDSのイベントカテゴリを調べる
    #################################
    paginator = client.describe_event_categories(SourceType = 'db-instance')
    for page in paginator['EventCategoriesMapList']:
        #############################################################################
        # 全てのイベントカテゴリから、自分が確認したいイベントカテゴリのみ抽出する
        # 確認したくないイベントカテゴリは、remove_targetに記載しておく
        #############################################################################
        all_event_category = page['EventCategories']
        remove_target = [
            'availability','backup','configuration change',
            'creation','deletion','notification','restoration'
        ]
        describe_event_category = []
        for all_event_category in all_event_category:
            if all_event_category not in remove_target:
                describe_event_category.append(all_event_category)
    ########################################################
    # イベントカテゴリを指定して、イベントログを確認する
    # イベントログは、現在～14日前までを表示する
    ########################################################
    now = datetime.now()
    two_weeks_ago = now - timedelta(days = 14)
    paginator = client.get_paginator('describe_events')
    page_iterator = paginator.paginate(
        EventCategories = describe_event_category,
        StartTime = two_weeks_ago,
        EndTime = now,
    )
    for page in page_iterator:
        for event_log in page['Events']:
            date = event_log['Date']
            source_identifier = event_log['SourceIdentifier']
            event_category = event_log['EventCategories']
            message = event_log['Message']
            print '{0: %Y-%m-%d-%H:%M} {1} {2} {3}'.format(
                date, source_identifier, event_category, message
            )

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 2):
        print 'example: python rds_event_describe.py [profile]'
        quit()
    profile = argvs[1]

    rds_event_describe(profile)
