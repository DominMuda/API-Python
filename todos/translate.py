import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1', use_ssl=True)
    translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )


    input_text = result['Item']['text']
    detected_language = comprehend.detect_dominant_language(Text = input_text)
    target_language = event['pathParameters']['language']
    

    #resultTx = translate.translate_text(Text=text, SourceLanguageCode=detected_language, TargetLanguageCode=target_language)

    # create a response
    #response = {
    #   "statusCode": 200,
    #    "body": json.dumps(result['Item'],
    #                       cls=decimalencoder.DecimalEncoder)
    #}
    
    response = {
        "statusCode": 200,
        "body": json.dumps(detected_language['Languages'][0]['LanguageCode'],
                        cls=decimalencoder.DecimalEncoder)

    }

    return response
