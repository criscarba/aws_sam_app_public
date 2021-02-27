import json
import os
from pydantic import BaseModel, ValidationError, validator, AnyUrl, Field
import services.event_check

def respond(err, res=None):
    return {
        'statusCode': '404' if err else '200',
        'body': json.dumps({"message": res}),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):
    operations = {
        'POST': lambda x: postMethodFunction(x),
        'GET': lambda x: respond('404','Unsupported method GET for this API')
        }
    json_region = os.environ['AWS_REGION']
    http_method = event['httpMethod']
    return operations[http_method](event['body'] if 'body' in event else '')

def postMethodFunction(payload):
    try:
        body_json = json.loads(payload) 
        parsed_event = services.event_check.payload_format(**body_json)
    except ValidationError as exc:
        respond('404', str(exc))
    except:
        respond('404', 'Unexpected Body Format')

    respond('','Payload Received Successfully TABLE: {} and ID: {}'.format(parsed_event.table, parsed_event.id))
