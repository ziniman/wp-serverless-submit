import json
import boto3
import os
from botocore.exceptions import ClientError
import logging
import base64
from send_email import send_email

logger = logging.getLogger()
logger.setLevel(logging.INFO)

kms = boto3.client('kms')
session = boto3.session.Session()

allowed_origins = kms.decrypt(CiphertextBlob=bytes(base64.b64decode(os.environ['AllowedDomains'])))['Plaintext'].decode("utf-8")
recipient = kms.decrypt(CiphertextBlob=bytes(base64.b64decode(os.environ['Recipient'])))['Plaintext'].decode("utf-8")

logger.info(allowed_origins)

allowed_origins = allowed_origins.split(",")
allowed_origins = list(map(str.strip, allowed_origins))

def check_origin(origin):
    logger.info('Origin: ' + origin)

    if origin in allowed_origins:
        return origin
    else:
        return False

def lambda_handler(event, context):

    logger.info('Event Data: ' + json.dumps(event))

    approved_origin = None
    origin = event['headers'].get('origin', '') or event['headers'].get('Origin', '')
    if origin:
        approved_origin = check_origin(origin)

    if approved_origin:
        headers = event['headers']
        logger.info(headers)

        if event.get('isBase64Encoded', False):
            body = base64.b64decode(event.get('body', '')).decode('utf-8')
        else:
            body = event.get('body', '')

        if body:
            if not send_email(body, headers, recipient):
                return {
                    'statusCode': 500,
                    'body': json.dumps('Error Sending Email!')
                };
        else:
            return {
                'statusCode': 204,
                'body': json.dumps('Empty Body!')
            };

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': approved_origin,
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps('Success!')
        };
    else:
        return {
            'statusCode': 403,
            'body': json.dumps('Error!')
        };
