import json
import pika
import django
from sys import path
from os import environ
from stocks.rabbitmq import StockRpcServer

path.append('/stock_service/stock_service/settings.py')
environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_service.settings')
django.setup()

stock_service = StockRpcServer()
print("Consuming Started...")
stock_service.channel.start_consuming()
