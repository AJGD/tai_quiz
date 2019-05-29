"""Account urls"""
from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('privacy_policy/', views.show_privacy_policy, name='privacy_policy')
]
