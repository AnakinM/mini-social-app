from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import SignUpForm
from mainview.views import index as mainview_index

# Create your views here.
def index(request):
    return render(request, 'welcomeview/index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'welcomeview/signup.html', {'form': form})


def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return mainview_index(request)
    else:
        return HttpResponse("Authentication failed.")