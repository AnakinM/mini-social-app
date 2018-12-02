from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'welcomeview/index.html') #HttpResponse("Welcome to Mini Social App")