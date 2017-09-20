from __future__ import print_function

import json
import urllib
import boto3

print('Loading ec2 Tag Function')

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        result = gets3data(bucket, key)
        print(result + ',' + key)
        update_ec2_tag(result, key)
    except Exception as e:
        print(e)

def gets3data(bucket, key):
    try:
        s3 = boto3.resource('s3')
        result = s3.Object(bucket, key).get()['Body'].read()
        return result
    except Exception as e:
        print(e)

def update_ec2_tag(data, key):
    instanceID = key.split("/")[1]
    serverName = data.split(",")[0]
    #instanceType = data.split(",")[1]
    #availabilityZone = data.split(",")[2]
    try:
        ec2 = boto3.resource('ec2')
        ec2.create_tags(Resources=[instanceID], Tags=[{'Key': 'Name', 'Value': serverName}])
        #ec2.create_tags(Resources=[instanceID], Tags=[{'Key': 'instanceType', 'Value': instanceType}])
        #ec2.create_tags(Resources=[instanceID], Tags=[{'Key': 'availabilityZone', 'Value': availabilityZone}])
    except Exception as e:
        print(e)
