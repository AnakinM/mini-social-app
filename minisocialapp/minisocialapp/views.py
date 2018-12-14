from django.contrib.auth import logout
from django.conf import settings
from django.shortcuts import render, redirect

from welcomeview.views import index as welcomeview_index
from mainview.views import index as mainview_index

def is_user_logged_in(request):
    if not request.user.is_authenticated:
        return welcomeview_index(request)
    elif request.user.is_authenticated:
        return mainview_index(request)

def logout_view(request):
    logout(request)
    return redirect('home')#welcomeview_index(request)
