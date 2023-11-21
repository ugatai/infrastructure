import os
import json
import http.client
from urllib.parse import urlparse

def lambda_handler(event, context):
    print(json.dumps(event))
    
    endpoint_url = ''
    if 'ENDPOINT_URL' in os.environ:
        endpoint_url = os.environ['ENDPOINT_URL']

    parsed_url = urlparse(endpoint_url)
    
    postData = json.dumps({
        'text': event['Records'][0]['Sns']['Message']
    }).encode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'Content-Length': len(postData)
    }

    conn = http.client.HTTPSConnection(parsed_url.hostname, port=parsed_url.port)
    
    try:
        conn.request('POST', parsed_url.path, body=postData, headers=headers)
        response = conn.getresponse()
        
        data = response.read()
        print(data.decode('utf-8'))
        return {
            'statusCode': response.status,
            'body': data.decode('utf-8')
        }
    except Exception as e:
        print(f'Error: {e}')
        raise e
    finally:
        conn.close()