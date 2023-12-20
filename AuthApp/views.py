import os

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from .forms import RegistrationForm

BASE_URL = os.getenv('BACKEND_SERVICE_END_POINT')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('application:home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'AuthApp/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    context = {}
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            createdUser = form.save(commit=False)
            createdUser.password = make_password(createdUser.password)
            createdUser.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")
        else:
            context = {
                "form": form,
            }
            return render(request, 'AuthApp/register.html', context=context)

    form = RegistrationForm()
    context['form'] = form
    
    return render(request, 'AuthApp/register.html', context)