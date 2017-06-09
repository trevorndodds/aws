#!/usr/bin/env python
import json
import logging
import boto3

queueName = 's3-ec2-tag'
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S %Z')
logger = logging.getLogger(__name__)

def check_sqs(qn):
    logger.info('Connecting to SQS')
    session = boto3.session.Session()
    sqs = session.resource('sqs', use_ssl=True)
    queue = sqs.get_queue_by_name(QueueName=qn)
    ApproximateNumberOfMessages = queue.attributes.get('ApproximateNumberOfMessages')
    logger.info('Approx Number of Messages: %s' % queue.attributes.get('ApproximateNumberOfMessages'))
    if int(ApproximateNumberOfMessages) > 0:
    	messages = queue.receive_messages()
        logger.info('Found %s messages' % len(messages))
        for message in messages:
            data = json.loads(message.body)
            bucket = data['Records'][0]['s3']['bucket']['name']
            key = data['Records'][0]['s3']['object']['key']
            try:
                result = gets3data(bucket, key)
                logger.info( result + ',' + key)
                update_ec2_tag(result, key)
                message.delete()
            except Exception as e:
                logger.error( "Error:  {}".format(str(e)))
            # pp(data)


def gets3data(bucket, key):
    try:
        s3 = boto3.resource('s3')
        result = s3.Object(bucket, key).get()['Body'].read()
        return result
    except Exception as e:
        logger.error("Error:  {}".format(str(e)))


def update_ec2_tag(data, key):
    instanceID = key.split("/")[1]
    serverName = data.split(",")[0]
    instanceType = data.split(",")[1]
    availabilityZone = data.split(",")[2]
    try:
        ec2 = boto3.resource('ec2')
        ec2.create_tags(Resources=[instanceID], Tags=[{'Key': 'Name', 'Value': serverName}])
        ec2.create_tags(Resources=[instanceID], Tags=[{'Key': 'instanceType', 'Value': instanceType}])
        ec2.create_tags(Resources=[instanceID], Tags=[{'Key': 'availabilityZone', 'Value': availabilityZone}])
    except Exception as e:
        logger.error( "Error:  {}".format(str(e)))


def main():
    check_sqs(queueName)


if __name__ == '__main__':
    main()

