from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views

app_name = 'database'  # Пространство имен для приложения

urlpatterns = [
    path('', views.home, name='home'),
    path('database/', views.database_list, name='database_list'),
    path('database/create/', views.create_database, name='create_database'),
    path('database/<int:pk>/', views.database_detail, name='database_detail'),
    path('database/<int:pk>/add_object/', views.add_data_object, name='add_data_object'),

    # Новый маршрут для обработки выбранных файлов
    path('data_objects/process_selected/', views.process_selected_files, name='process_selected_files'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)