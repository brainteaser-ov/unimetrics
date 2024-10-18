from django.urls import path
from . import views

app_name = 'database'  # Пространство имен для приложения

urlpatterns = [
    path('', views.home, name='home'),
    path('databases/', views.database_list, name='database_list'),
    path('databases/create/', views.create_database, name='create_database'),
    path('databases/<int:pk>/', views.database_detail, name='database_detail'),
    path('databases/<int:pk>/add_object/', views.add_data_object, name='add_data_object'),
]
