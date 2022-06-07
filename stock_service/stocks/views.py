# encoding: utf-8

from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from .rabbitmq import decoder

class StockView(APIView):
    """
    Receives stock requests from the API service.
    """
    def get(self, request, *args, **kwargs):
        stock_code = request.GET.get("stock_code", "EmptyError")

        if stock_code == "EmptyError":
            json = {"Error": "Stock code is empty"}
            status = 204
            return Response(json, status)

        try:
            with requests.Session() as s:
                stock_raw_info = s.get(f'https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcvn&h&e=csv')
                json, status = decoder(stock_raw_info.content)
                
        except Exception as e:
            json = {"Error": "Unable to fetch stock information"}
            status = 500
        finally:
            return Response(json, status=status)
