from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Регистрация пользователя
    path('signup/', views.signup, name='signup'),
    # Вход пользователя
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # Выход пользователя
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    # Смена пароля
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),
    # Личный кабинет
    path('profile/', views.profile, name='profile'),
]