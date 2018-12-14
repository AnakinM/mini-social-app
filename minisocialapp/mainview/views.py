from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):
    if request.user.is_authenticated:
        return render(request, 'mainview/profile.html')
    else:
        return redirect('home')