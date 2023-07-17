from django.shortcuts import render
from .forms import CustomUserCreation
from django.contrib.auth import login as dj_login, authenticate, logout
# Create your views here.

def registration_view(request):
    context = []
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserCreation(request.POST)
            if form.is_valid():
                form.save()
                