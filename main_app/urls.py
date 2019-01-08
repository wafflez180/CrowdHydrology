from django.contrib import admin
from django.urls import path
from main_app import views, receive_sms, graphs

# Template Urls
app_name = 'main_app'

urlpatterns = [
    path('sms/', receive_sms.incoming_sms, name='sms'),
    path('', views.index, name='index'),
    path('generate-graphs/', graphs.generate, name='generate-graphs'),
    path('download/', views.download, name='download'),
    path('transfer/', views.transfer, name='transfer'),
    #path('user_login/', views.user_login, name='user_login')
]
