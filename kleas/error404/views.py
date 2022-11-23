from django.shortcuts import render
from django.http import HttpResponse


def error_404_view(request, exception):
    data = {"name": "Klea Sales and Expense Tracker"}
    return render(request,'error404/404.html', data)


def index(request):
    return HttpResponse("Hello, world. You're at the Home page of Django sample project error 404.")