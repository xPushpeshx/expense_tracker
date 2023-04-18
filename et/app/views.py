from django.shortcuts import render ,HttpResponseRedirect , redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login(request):
    return render(request, 'login.html', {})

def add(request):
    return render(request, 'add.html', {})

def base(request):
    return render(request, 'base.html', {})

def home(request):
    return render(request, 'home.html', {})

def display(request):
    return render(request, 'display.html', {})

def edit(request):
    return render(request, 'edit.html', {})

def homepage(request):
    return render(request, 'homepage.html', {})

def limit(request):
    return render(request, 'limit.html', {})

def signup(request):
    return render(request, 'signup.html', {})

def year(request):
    return render(request, 'year.html', {})
