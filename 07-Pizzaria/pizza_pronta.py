import json
import boto3
from baseDAO import BaseDAO

def lambda_handler(event, context):
    try:
        # Ler evento do EventBridge
        event_details = event.get('detail', {})
        print(event_details)

        status = event_details.get('status')
        if status:
            pedido = event_details.get('pedido')
            cliente = event_details.get('cliente')
            
            if status.lower() == 'pronto':
                sqs = boto3.client('sqs')
                queue_url = 'arn:aws:sqs:us-east-1:186019336293:espera-entrega'

                # Enviar uma mensagem para a fila SQS
                response = sqs.send_message(
                    QueueUrl=queue_url,
                    MessageBody=f'Pedido {pedido} pronto para entrega!'
                )

                # Grava o evento na tabela DynamoDB
                item = {
                    "pedido": str(pedido),
                    "status": status,
                    "cliente": cliente,
                    "time": event.get('time')
                }

                dao = BaseDAO('eventos-pizzaria')
                responseDB = dao.put_item(item)
                print(responseDB)

        return True
    except Exception as e:
        print("Erro:", str(e))
        return False
