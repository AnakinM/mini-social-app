from django.urls import path

from . import views

app_name = 'welcomeview'
urlpatterns = [
    path('', views.index, name='index'),
]