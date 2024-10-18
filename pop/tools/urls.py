from django.urls import path
from . import views

app_name = 'tools'  # Пространство имен для приложения

urlpatterns = [
    path('', views.home, name='home'),
    path('text-analysis/', views.text_analysis, name='text_analysis'),
    path('create-specification/', views.create_specification, name='create_specification'),
    path('create-neural-network/', views.create_neural_network, name='create_neural_network'),
]