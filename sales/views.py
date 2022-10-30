from django.views.generic import ListView, UpdateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from .models import Sale, Item, Category, PaymentType
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# list sale instances class-based view
class SaleTransactions(LoginRequiredMixin, ListView):
    model = Sale
    queryset = Sale.objects.order_by('-purchase_date')
    template_name = 'sales/transactions.html'
    context_object_name = 'sales'

# edit sale record
@login_required
def edit(request, pk):
    sale = Sale.objects.get(id=pk)
    context = {
        'title': 'Edit Sale',
        'sale': sale,
    }
    return render(request, 'sales/edit.html', context=context)

# update sale record
@login_required
def update(request, pk):
    sale = Sale.objects.get(id=pk)
    sale.price = request.POST['price']
    sale.quantity = request.POST['quantity']
    sale.payment = PaymentType.objects.get(id=request.POST['payment'])
    sale.category = Category.objects.get(id=request.POST['category'])
    sale.item = Item.objects.get(id=request.POST['item'])
    sale.save()
    return redirect(reverse('sales:transactions'))

# delete sale instance function-based view
@login_required
def delete(request, pk):
    sale = Sale.objects.get(id=pk)
    sale.delete()
    return redirect(reverse('sales:transactions'))

# add sale instance function-based view
@login_required
def add(request):

    # template (add.html) title
    context = {'title': 'Add Sales'}

    # check if request is POST, if yes, save the sale transaction 
    if request.method == 'POST':
        saleObj = Sale()
        saleObj.price = request.POST['price']
        saleObj.quantity = request.POST['quantity']
        saleObj.payment = PaymentType.objects.get(id=request.POST['payment'])
        saleObj.category = Category.objects.get(id=request.POST['category'])
        saleObj.item = Item.objects.get(id=request.POST['item'])
        saleObj.save()
        messages.success(request, 'Sale Transaction Saved!')
        return redirect(reverse('sales:add'))
    # else only render empty form
    else:
        return render(request, 'sales/add.html', context=context)

# helper function for loading clothes item based on category
@login_required
def load_items(request):
    category_id = request.GET['category']
    items = Item.objects.filter(category_id=category_id).order_by('item')
    return render(request, 'sales/item_options.html', context={'items': items})
