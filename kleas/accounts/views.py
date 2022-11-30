from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, admin_only

from . forms import CreateUserForm

@login_required
@admin_only
def registerPage(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group, created = Group.objects.get_or_create(name=str(request.POST.get('group')))
            user.groups.add(group)
            
            messages.success(request, f'Account was created for {username}')

            return redirect(reverse('accounts:login'))
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
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

@admin_only
def contacts(request):
    return render(request, 'accounts/contact.html')


