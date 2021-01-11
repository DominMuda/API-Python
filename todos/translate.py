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


    text = "It is raining today in Seattle"
    print('Calling DetectDominantLanguage')
    detected_language = comprehend.detect_dominant_language(Text = text)

    print(detected_language)

    target_language = event['pathParameters']['language']
    

    resultTx = translate.translate_text(Text='Hello, World', SourceLanguageCode='en', TargetLanguageCode='es')

    # create a response
    #response = {
    #   "statusCode": 200,
    #    "body": json.dumps(result['Item'],
    #                       cls=decimalencoder.DecimalEncoder)
    #}
    
    response = {
       "statusCode": 200,
        "body": json.dumps(detected_language,
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
