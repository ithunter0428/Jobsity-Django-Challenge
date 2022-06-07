# encoding: utf-8

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.models import UserRequestHistory
from api.serializers import UserRequestHistorySerializer, UserSerializer
from django.db.models import Count
import requests
from .rabbitmq import StockRpcClient

stock_service = StockRpcClient()

class UserCreateView(CreateAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = UserSerializer

class StockView(APIView):
    """
    Endpoint to allow users to query stocks
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserRequestHistorySerializer

    def get(self, request, *args, **kwargs):
        stock_code = request.GET.get("q", "EmptyError")

        if stock_code == "EmptyError":
            json = {"Error": "Stock code is empty"}
            status = 204
            return Response(json, status)

        try:
            # Using Http
            # with requests.Session() as s:
            #     response = requests.request("GET", "http://127.0.0.1:8001/stock", params={'stock_code': f'{stock_code}'})
            #     if response.status_code == 200:
            #         allData = response.json()
            #         self.save_query_to_db(allData, request.user)
            
            #         # serializer = self.serializer_class(allData)
            #         # data = serializer.data
            #         # return Response(data=data, status=200)

            #         return Response(data=allData, status=200)
            #     else:
            #         return Response(data=response.json(), status=response.status_code)
            
            # Using RabbitMQ
            data, status = stock_service.get_stock({'stock_code': stock_code})
            
            if status == 200:
                self.save_stock_data(data, request.user)
            return Response(data=data, status=status)
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
    def save_stock_data(self, stockData, user):
        userRequestHistory = UserRequestHistory()
        userRequestHistory.user = user
        userRequestHistory.date = stockData["Date"] + "T" + stockData["Time"] + "Z"
        userRequestHistory.name = stockData["Name"]
        userRequestHistory.symbol = stockData["Symbol"]
        userRequestHistory.open = stockData["Open"]
        userRequestHistory.high = stockData["High"]
        userRequestHistory.low = stockData["Low"]
        userRequestHistory.close = stockData["Close"]
        userRequestHistory.save()

class HistoryView(generics.ListAPIView):
    """
    Returns queries made by current user.
    """
    queryset = UserRequestHistory.objects.all()
    serializer_class = UserRequestHistorySerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        queryset = self.queryset.filter(user_id=user_id).order_by('-date')
        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=200)

class StatsView(APIView):
    """
    Allows super users to see which are the most queried stocks.
    """
    permission_classes = (IsAuthenticated,)
    queryset = UserRequestHistory.objects.all()

    def get(self, request, *args, **kwargs):

        if not request.user.is_superuser:
            return Response({"error": "You are not authorized to access this endpoint"}, status=403)

        queryset = self.queryset.values('symbol', 'name').annotate(times_requested=Count('name')).order_by('-times_requested')[:5]

        return Response(data=queryset, status=200)
