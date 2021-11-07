import json
import os
import boto3
import logging

# import requests


def __init():
    event = {'resource': '/doc-generator', 'path': '/doc-generator', 'httpMethod': 'POST', 'headers': None, 'multiValueHeaders': None, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'a7j9hu', 'resourcePath': '/doc-generator', 'httpMethod': 'POST', 'extendedRequestId': 'IdQhOFUMIAMFYYg=', 'requestTime': '07/Nov/2021:23:28:58 +0000', 'path': '/doc-generator', 'accountId': '668721781078', 'protocol': 'HTTP/1.1', 'stage': 'test-invoke-stage', 'domainPrefix': 'testPrefix', 'requestTimeEpoch': 1636327738890, 'requestId': '5a1fe4b8-92f6-4281-be54-6140723f77b4', 'identity': {'cognitoIdentityPoolId': None, 'cognitoIdentityId': None, 'apiKey': 'test-invoke-api-key', 'principalOrgId': None, 'cognitoAuthenticationType': None, 'userArn': 'arn:aws:iam::668721781078:user/tom', 'apiKeyId': 'test-invoke-api-key-id', 'userAgent': 'aws-internal/3 aws-sdk-java/1.12.76 Linux/5.4.134-73.228.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.302-b08 java/1.8.0_302 vendor/Oracle_Corporation cfg/retry-mode/standard', 'accountId': '668721781078', 'caller': 'AIDAZXMXMTFLGLL3GANQT', 'sourceIp': 'test-invoke-source-ip', 'accessKey': 'ASIAZXMXMTFLBHNXXIF3', 'cognitoAuthenticationProvider': None, 'user': 'AIDAZXMXMTFLGLL3GANQT'}, 'domainName': 'testPrefix.testDomainName', 'apiId': 'jcckpg5yx7'}, 'body': '{\n        "template": "meutemplate.html",\n        "variables": {\n            "nome": "Fulanto de Tal",\n            "cpf": "123.456.789-04"\n        }\n    }', 'isBase64Encoded': False}
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
    logging.getLogger().setLevel(logging.INFO)

    logging.info("event=%s", event)

    bucket = os.environ['TemplatesS3Bucket'] # this comes from template.yml configuration and its set on ci/cd time
    logging.info("bucket=%s",bucket)

    body = json.loads(event["body"])

    template = body['template']
    logging.info("template=%s",template)

    variables = body['variables'] #dict
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