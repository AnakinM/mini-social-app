from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, render_to_response
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm

from .forms import UserRegisterForm
from mainview.models import Post

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f'Your account has been successfuly created.')
            return redirect('mainview:home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('mainview:home')
        else:
            return render(request, 'users/login.html', {'username': username, 'error': True})
    else:
        return render(request, 'users/login.html', {})

def ProfileDetailsView(request, username):
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)

        posts = Post.objects.filter(author=user.pk)

        gender = ''
        if user.profile.gender == 'M':
            gender='Male'
        elif user.profile.gender == 'F':
            gender='Female'
            
        data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'gender': gender,
            'age': user.profile.age,
            'town': user.profile.town,
            'country': user.profile.country,
            'company': user.profile.company,
            'image': user.profile.image,
            'posts': posts,
        }
        return render(request, 'users/profile_details.html', data)
    else:
        messages.warning(request, f'There is no user of that username.')
        return redirect('mainview:home')

@login_required
def ProfileEditView(request, username):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated.')
            return redirect('mainview:home')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile_edit.html', context)

