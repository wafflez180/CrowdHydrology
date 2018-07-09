from django.contrib import admin
from django.urls import path
from main_app import views, receive_sms

# Template Urls
app_name = 'main_app'

urlpatterns = [
    #path('sms/', receive_sms.incoming_sms, name='sms'),
    #path('register/', views.register, name='register'),
    #path('user_login/', views.user_login, name='user_login')
]
