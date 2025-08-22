import json
import boto3

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        customer_phone = body['phoneNumber']
        recording_consent = body.get('recordingConsent', 'NO')
        
        connect = boto3.client('connect')
        
        response = connect.start_outbound_voice_contact(
            DestinationPhoneNumber='+XXXXXXXXXX',  # AWS Number assigned to the callback Queue. This is needed as AWS connect.start_outbound_voice_contact always calls the number right away, so we lead them into the flow first where we change the number to the customer to receive a callback.
            ContactFlowId='XXXXXXXXXXXX',  # Your callback flow ID (Found under About this Flow, inside the Amazon Connect flow)
            InstanceId='XXXXXXXXXXXX',     # Your Instance ID (Can also be found under About this Flow, inside the Amazon Connect flow, right before the flow ID)
            QueueId='XXXXXXXXXXXX',        # Your callback queue ID (Found under Show additional queue information, inside the Amazon Connect queue)
            Attributes={
                'CustomerPhone': customer_phone,  # Real customer number
                'recordingConsent': recording_consent,
                'CallbackSource': 'WebForm'
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': 'Callback queued successfully!',
                'contactId': response['ContactId']
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
