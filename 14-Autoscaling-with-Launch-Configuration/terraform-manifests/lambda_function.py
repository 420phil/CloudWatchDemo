import boto3
import json
import os

sns_client = boto3.client('sns')


def lambda_handler(event, context):
    for record in event['Records']:
        # Check if the event is a security group modification
        if (record['eventName'] == 'AuthorizeSecurityGroupIngress' or
            record['eventName'] == 'AuthorizeSecurityGroupEgress' or
            record['eventName'] == 'RevokeSecurityGroupIngress' or
                record['eventName'] == 'RevokeSecurityGroupEgress'):

            # Get the details of the security group modification event
            event_time = record['eventTime']
            event_name = record['eventName']
            security_group_id = record['responseElements']['groupId']
            region = record['awsRegion']
            user_identity = record['userIdentity']['principalId']

            # Send an email notification using SNS
            sns_topic_arn = os.environ['SNS_TOPIC_ARN']
            message = f"Security group {security_group_id} was modified by {user_identity} at {event_time} ({event_name})."
            subject = f"Security group modification in {region}"
            sns_client.publish(
                TopicArn=sns_topic_arn,
                Message=message,
                Subject=subject
            )
