from typing import List
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from .models import Sale, Item, Category, PaymentType


def add(request):
    if request.method == "POST":
        saleObj = Sale()
        saleObj.price = request.POST["price"]
        saleObj.quantity = request.POST["quantity"]
        saleObj.payment = PaymentType.objects.get(id=request.POST["payment"])
        saleObj.category = Category.objects.get(id=request.POST["category"])
        saleObj.item = Item.objects.get(id=request.POST["item"])
        saleObj.save()

        messages.success(request, "Sale Transaction Saved!")

        return redirect(reverse("sales:add"))
    else:
        return render(request, "sales/add.html")


class SaleTransactions(ListView):
    model = Sale
    template_name = "sales/transactions.html"
    context_object_name = "sales"


def load_items(request):
    category_id = request.GET.get('category')
    items = Item.objects.filter(category_id=category_id).order_by('item')
    return render(request, 'sales/item_options.html', context={'items': items})

def success(request):
    return render(request, 'sales/success.html')
