"""
URL configuration for pop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from database import views as database_views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  # path('', views.home, name='home'),

                  # Подключаем маршруты приложения 'database'
                  path('database/', include('database.urls', namespace='database')),
                  path('', database_views.home, name='home'),

                  # Подключаем маршруты приложения 'tools'
                  path('tools/', include('tools.urls', namespace='tools')),
                  path('accounts/', include('django.contrib.auth.urls')),

                  path('accounts/', include('accounts.urls', namespace='accounts')),
                  # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
                  # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

                  # корневой маршрут
                  # path('', views.homepage, name='homepage'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
