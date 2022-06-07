# encoding: utf-8

from django.contrib import admin
from django.urls import path, include

from api import views as api_views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin', admin.site.urls),
    path('user/create/', api_views.UserCreateView.as_view()),
    path('stock', api_views.StockView.as_view()),
    path('history', api_views.HistoryView.as_view()),
    path('stats', api_views.StatsView.as_view()),
    path('api/token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
