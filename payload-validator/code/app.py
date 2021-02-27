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
    # operations = {
    #     'create': lambda x: dynamo.put_item(**x),
    #     'read': lambda x: dynamo.get_item(**x),
    #     'update': lambda x: dynamo.update_item(**x),
    #     'delete': lambda x: dynamo.delete_item(**x),
    #     'list': lambda x: dynamo.scan(**x),
    #     'echo': lambda x: x,
    #     'ping': lambda x: 'pong'
    # }

    # operations = {
    #     'POST': lambda x: postMethodFunction(**x) ,
    #     'GET': return respond('404','Unsupported method GET for this API')}
    operations = {
        'POST': lambda x: postMethodFunction(x),
        'GET': lambda x: respond('404','Unsupported method GET for this API')}
    json_region = os.environ['AWS_REGION']
    http_method = event['httpMethod']
    if 'body' in event:
        print('SI HAY BODY')
    else:
        print('NO HAY BODY')
    return operations[http_method](event['body'] if 'body' in event else '')

    # ##### Validación de Evento #####
    # # 1) Valicación de API Call
    # # if http_method not in operations:
    # #     return respond('404','Unsupported method GET for this API')

    # # 2) Validación de Parseo y formato del Body
    # print(event['body'])
    # try:
    #     body_json = json.loads(event['body']) 
    #     print(body_json)
    #     parsed_event = services.event_check.payload_format(**body_json)
    # except ValidationError as exc:
    #     return respond('404', str(exc))
    # except:
    #     return respond('404', 'Unexpected Body Format')

    # return respond('','Payload Received Successfully TABLE: {} and ID: {}'.format(parsed_event.table, parsed_event.id))

def postMethodFunction(payload):
    print('llegue')
    print(payload)
    try:
        body_json = json.loads(payload) 
        print(body_json)
        parsed_event = services.event_check.payload_format(**body_json)
    except ValidationError as exc:
        return respond('404', str(exc))
    except:
        return respond('404', 'Unexpected Body Format')

    return respond('','Payload Received Successfully TABLE: {} and ID: {}'.format(parsed_event.table, parsed_event.id))

