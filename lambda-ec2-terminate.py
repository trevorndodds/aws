import json
import boto3
import datetime

def get_ec2():
    try:
        ec2 = boto3.resource('ec2')
        instances = ec2.instances.filter(
                Filters=[{'Name': 'tag:', 'Values': ['']}])
                #Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for instance in instances:
          if instance.tags:
           for i in range(len(instance.tags)):
            if instance.tags[i]['Key'] == "Name":
             instance_name = instance.tags[i]['Value']
             print "%s, %s, %s, %s" % (instance_name, instance.id, instance.instance_type, instance.launch_time)
             result = get_time(instance.launch_time, instance_name)
             if result:
              response = ec2_terminate(instance.id)
              print response
    except Exception as e:
        print(e)

def get_time(launch_time, instanceName):
    try:
             current_time = datetime.datetime.now(launch_time.tzinfo)
             running_time = current_time - launch_time
             print "%s - Total Running Time: %s " % (instanceName, running_time)
             if running_time.days>1:
              print "%s - Older than 1 day - starting termination" % instanceName
              return True
             else:
              print "%s - Less than 1 day" % instanceName
              return False
    except Exception as e:
        print(e)

def ec2_terminate(instanceID):
    try:
        ec2 = boto3.resource('ec2')
        instance = ec2.Instance(instanceID)
        response = instance.terminate()
        return response
    except Exception as e:
        print(e)


def main(event, context):
    get_ec2()

if __name__ == '__main__':
    main()
