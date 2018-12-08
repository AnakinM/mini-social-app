from django.urls import path

from . import views

app_name = 'mainview'
urlpatterns = [
    path('', views.index, name='profile'),
]