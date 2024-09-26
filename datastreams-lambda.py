import json
import boto3
import base64

def lambda_handler(event, context):
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data'])
        de_serialize_payload = json.loads(payload)
        print("de_serialize_payload", de_serialize_payload, type(de_serialize_payload))
