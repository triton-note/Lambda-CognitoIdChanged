from __future__ import print_function

import boto3
import json

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    tableName = event['table_name']
    preValue = event['previous']
    curValue = event['current']

    primary = 'COGNITO_ID'
    table = boto3.resource('dynamodb').Table(tableName)
    secondary = filter(lambda x: x != primary, map(lambda x: x['AttributeName'], table.key_schema))[0]
    print("Secondary key: " + secondary)
    founds = table.query(KeyConditionExpression=boto3.dynamodb.conditions.Key(primary).eq(preValue))

    updates = []
    for item in founds['Items']:
        key = item[secondary]
        updates.append(key)
        print("Updating: " + key)
        item[primary] = curValue
        table.put_item(Item=item)
        table.delete_item(Key={primary: preValue, secondary: key})
    return updates
