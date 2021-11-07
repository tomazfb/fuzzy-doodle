import json
import os
import boto3
import logging

# import requests


def __init():
    event = {
        "template": "meutemplate.html",
        "variables": {
            "nome": "Fulanto de Tal",
            "cpf": "123.456.789-01"
        }
    }
    os.environ["TemplatesS3Bucket"] = "fuzzy-doodle-templates"

    lambda_handler(event, None)

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    logging.basicConfig(level=logging.INFO)

    logging.info("event=%s", event)

    bucket = os.environ['TemplatesS3Bucket'] # this comes from template.yml configuration and its set on ci/cd time
    logging.info("bucket=%s",bucket)

    template = event['template']
    logging.info("template=%s",template)

    variables = event['variables'] #dict
    logging.info("variables=%s", variables)

    s3 = boto3.client('s3')
    s3_object = s3.get_object(Bucket=bucket, Key=template)
    body = s3_object['Body']
    content = body.read()
    

    ## read template
    result = str(content)
    for key, value in variables.items():
        result = result.replace("${"+key+"}", value)

    #log.info(result)
    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    return {
        "statusCode": 200,
        "body": result
        #json.dumps({
        #    "message": "hello world",
        #    # "location": ip.text.replace("\n", "")
        #}),
    }


#__init()