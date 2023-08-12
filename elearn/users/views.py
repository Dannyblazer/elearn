from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import CustomUserCreation
from django.db.models import Q
from django.contrib.auth import login as dj_login, authenticate, logout
from .forms import AccountAuthenticationForm, AccountUpdateForm
from .models import Account
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

def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            email.lower()
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                dj_login(request, user)
                return redirect('home')
    
    else:
        form = AccountAuthenticationForm()
    return render(request, 'users/login.html', context={'form':form})

def logout_view(request):
    logout(request)
    return redirect('home')

def must_authenticate_view(request):
    return render(request, "users/must_authenticate.html", context={})

def edit_account(request, *args, **kwargs):
	if not request.user.is_authenticated:
		return redirect("users:must_authenticate")
	user_id = kwargs.get("user_id")
	account = Account.objects.get(pk=user_id)
	if account.pk != request.user.pk:
		return HttpResponse("You cannot edit someone elses profile.")
	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect("users:profile", user_id=account.pk)
		else:
			form = AccountUpdateForm(request.POST, instance=request.user,
				initial={
					"user_id": account.pk,
					"email": account.email
				}
			)
			context['form'] = form
	else:
		form = AccountUpdateForm(
			initial={
					"user_id": account.pk,
					"email": account.email, 
					"username": account.username,
				}
			)
		context['form'] = form
	return render(request, "users/account.html", context)

# Remember to modify the search from users to courses

def account_search_view(request, *args, **kwargs):
    context = {}

    if request.method == 'GET':
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            search_results = Account.objects.filter(
			Q(email__contains=search_query)|
			Q(username__icontains=search_query)
			).distinct()
            accounts = []
            for account in search_results:
                if request.user in account.user.friends.all():
                    accounts.append((account, True))
                else:
                    accounts.append((account, False))
            context['accounts'] = accounts
        

    return render(request, "users/search_results.html", context)
