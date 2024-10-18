from django.urls import path
from . import views

app_name = 'tools'  # Пространство имен для приложения

urlpatterns = [
    # Пример маршрутов для приложения tools
    path('', views.home, name='home'),
    path('execute/', views.execute_tool, name='execute_tool'),
    # Добавьте другие маршруты вашего приложения
]