import json
import pika
import requests
import csv

class StockRpcServer(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=600, blocked_connection_timeout=300))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='stock_service')
        self.callback_queue = result.method.queue

        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.callback, auto_ack=True)

    def callback(self, ch, method, properties, body):
        print("Received in Stock_Service...")
        params = json.loads(body)
        print("params", params)

        if properties.content_type == 'get_stock':
            stock_code = params['stock_code']
            print("stock_code", stock_code)

            if stock_code == "EmptyError":
                print({"Error": "Stock code is empty"})
                
            try:
                response = requests.request("GET", f'https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcvn&h&e=csv')
                print("stock_response", response.content)
                data, status = decoder(response.content)
                
                if (status == 200):
                    self.channel.basic_publish(
                        exchange='',
                        routing_key='api_service',
                        body=json.dumps({'data': data, 'status': status}),
                        properties=pika.BasicProperties(correlation_id=properties.correlation_id)
                    )
                    print("stock result replied")
                
            except Exception as e:
                print({"Error": str(e)})
            finally:
                print("finally")
            
        print("receive finished")

def decoder(data):
    decoded = data.decode('utf-8')
    rows = [x for x in csv.reader(decoded.splitlines(), delimiter=',')]
    symbol, date, time, open, high, low, close, volume, name = rows[1]
    if open == 'N/D':
        json = {"Error": "Unable to find stock"}
        status = 404
    else:
        json = {"Symbol": f"{symbol}", "Date": f"{date}", "Time": f"{time}", "Open": f"{open}",
                "High": f"{high}", "Low": f"{low}", "Close": f"{close}", "Volume": f"{volume}", "Name": f"{name}"}
        status = 200
    return json, status
