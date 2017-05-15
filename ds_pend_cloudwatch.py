#!/usr/bin/env python
import os
import sys
import time
import boto3
from suds.client import Client

interval = 60

# Grid Creds for SOAP connection
dsURL = ''
gridUser = ''
gridPassword = ''


def push_metric_to_cloudwatch(pendingTasks):
    print 'Sending %s to cloudwatch' % pendingTasks
    session = boto3.session.Session()
    cloudwatch = session.client('cloudwatch', use_ssl=False)
    cloudwatch.put_metric_data(
    Namespace='TD/DataSynapse',
    MetricData=[
            {
                'MetricName': 'PendingTasks',
                'Dimensions': [
                    {'Name': 'Per-Grid Metrics',
                     'Value': 'DEV'},
                ],
                'Unit': 'Count',
                'Value': pendingTasks
            }
        ]
    )


def check_ds_pending_tasks():
    try:
        ds_client = Client(url=dsURL + '/livecluster/webservices/ManagerAdmin?wsdl',
                           username=gridUser, password=gridPassword)
        pending_tasks = ds_client.service.getPendingInvocationCount()
        push_metric_to_cloudwatch(pending_tasks)
    except:
        pass


def main():
    check_ds_pending_tasks()


if __name__ == '__main__':
    try:
        nextRun = 0
        while True:
                if time.time() >= nextRun:
                        nextRun = time.time() + interval
                        now = time.time()
                        main()
                        elapsed = time.time() - now
                        print "Total Elapsed Time: "+str(elapsed)
                        timeDiff = nextRun - time.time()
                        time.sleep(timeDiff)
    except KeyboardInterrupt:
        print 'Interrupted'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
