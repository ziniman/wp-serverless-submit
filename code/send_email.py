import json
import boto3
from botocore.exceptions import ClientError
import logging
import email.parser
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

region = os.environ['AWS_REGION']

def send_email(post, headers, recipient):
    full_header = "Content-Type: " + headers['content-type'] + "\n\r"
    post = full_header + post
    logger.info(post)

    msg = email.parser.Parser().parsestr(post)

    data = {}
    for part in msg.get_payload():
        data.update({(part.get_param('name', header='content-disposition')):(part.get_payload(decode=False))})

    logger.info(data)

    body = 'New form submission recived from %s (%s)\n\n' % (headers.get('origin', 'NO-ORIGIN'), headers.get('x-forwarded-for', "NO-IP"))

    for key, value in data.items():
        body+= "%s: %s\n" % (key, value)

    logger.info(body)

    RECIPIENT = recipient
    SENDER = "WPSS Mailer<" + RECIPIENT + ">"


    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = region

    # The subject line for the email.
    SUBJECT = "Email from WPSS"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = (body)

    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      """ + body.replace("\n", "<br />") + """
    </body>
    </html>
                """

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        return False
    else:
        logger.info("Email sent! Message ID:"),
        logger.info(response['MessageId'])
        return True
