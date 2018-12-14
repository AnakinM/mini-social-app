from django.urls import path

from . import views

app_name = 'welcomeview'
urlpatterns = [
    path('', views.index, name='welcome-home'),
    path('signup/', views.signup, name='signup-view'),
    path('login/', views.login_user, name='login-view'),
]