from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
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
                email = form.cleaned_data('email')
                raw_password = form.cleaned_data('password')
                account = authenticate(email=email, password=raw_password)
                dj_login(request, account)
                return HttpResponseRedirect(reverse('home'))
            else:
                context['registration_form'] = form
        else:
            form = CustomUserCreation
            context['registration_form'] = form
        return render(request=request, template_name='users/register.html', context={'registration_form':form})
    else:
        return redirect('home')
    