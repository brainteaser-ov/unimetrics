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
    path('database/<int:pk>/edit/', views.update_database, name='update_database'),
    path('database/<int:pk>/delete/', views.delete_database, name='delete_database'),
    path('database/<int:db_pk>/object/<int:pk>/edit/', views.edit_data_object, name='edit_data_object'),
    path('database/<int:db_pk>/object/<int:pk>/delete/', views.delete_data_object, name='delete_data_object'),
    path('database/contact/', views.contact_view, name='contact'),
    path('data_objects/process_selected/', views.process_selected_files, name='process_selected_files'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
