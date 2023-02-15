from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # don't neet to def in views.py

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'), # localhost:8000/users/register/
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'), #localhost:8000/users/login/
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
]