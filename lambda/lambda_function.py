from __future__ import print_function

import json
import decimal
import os
import boto3
from botocore.exceptions import ClientError
import requests
import uuid
from datetime import datetime, timezone, timedelta

# set environment variable
TABLE_NAME = os.environ['TABLE_NAME']

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

# set coincheck variable
RATE_URL = 'https://coincheck.com/api/exchange/orders/rate'
coins = {'BTC': 'btc_jpy', 'ETC': 'etc_jpy', 'FCT': 'fct_jpy', 'MONA': 'mona_jpy'}


def lambda_handler(event, context):
    
    for key, item in coins.items():
        # get rate
        params = {'order_type': 'sell', 'pair': item, 'amount': 1}
        coincheck = requests.get(RATE_URL, params=params).json()

        # create item dict
        item = {
            'id': key,
            'timestamp': decimal.Decimal(int(datetime.now(timezone(timedelta(hours=9))).timestamp())),
            'rate': decimal.Decimal(coincheck['rate']),
            'created_at': datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')
        }
        print(item)

        # put item in table
        table.put_item(Item = item)

    return {
        'statusCode': 200
    }

# this custom class is to handle decimal.Decimal objects in json.dumps()
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

