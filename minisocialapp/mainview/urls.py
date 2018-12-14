from django.urls import path

from . import views
from minisocialapp import views as minisocialapp_views

app_name = 'mainview'
urlpatterns = [
    path('', views.index, name='profile'),
]