import json
import pika
import uuid

class StockRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=600, blocked_connection_timeout=300))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='api_service', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)

    def on_response(self, ch, method, props, body):
        print("received", body)
        print("received", props.correlation_id)
        if self.corr_id == props.correlation_id:
            self.response = body

    def get_stock(self, body):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        print("sent", self.corr_id)
        self.channel.basic_publish(
            exchange='',
            routing_key='stock_service',
            properties=pika.BasicProperties(content_type='get_stock', reply_to=self.callback_queue, correlation_id=self.corr_id),
            body=json.dumps(body),
        )
        
        while self.response is None:
            self.connection.process_data_events()
        
        print("received")
        
        response_json = json.loads(self.response)
        data = response_json['data']
        status = response_json['status']
        return data, status
