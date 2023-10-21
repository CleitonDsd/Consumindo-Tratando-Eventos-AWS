import json
import boto3

# Configurar a conexão com a fila SQS
sqs = boto3.client('sqs')
queue_url = 'arn:aws:sqs:us-east-1:186019336293:espera-entrega' 

def handler(event, context):
    try:
        # Receber mensagens da fila SQS
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[
                'All'
            ],
            MessageAttributeNames=[
                'All'
            ],
            MaxNumberOfMessages=1,  # processar uma mensagem de cada vez
            VisibilityTimeout=0,
            WaitTimeSeconds=0
        )
        
        if 'Messages' in response:
            message = response['Messages'][0]
            receipt_handle = message['ReceiptHandle']
            
            
            #exclui a mensagem da fila após processamento
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
        
        return {
            'statusCode': 200,
            'body': 'Mensagem da fila SQS processada com sucesso!'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'Erro no processamento da mensagem da fila SQS. Consulte os logs para obter mais detalhes.'
        }
