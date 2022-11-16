from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from . forms import CreateUserForm

# Create your views here.

def registerPage(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {user}')

            return redirect(reverse('accounts:login'))
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse('sales:add'))
        else:
            messages.info(request, 'Username or Password Is Incorrect')

    return render(request, 'accounts/login.html')

def logoutUser(request):
    logout(request)
    return redirect(reverse('accounts:login'))

def contacts(request):
    return render(request, 'accounts/contact.html')


