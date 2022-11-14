from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from . models import Sale, Item
from . forms import SaleForm

# Create your views here.

class SaleCreateView(SuccessMessageMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sales/sale_form.html'
    success_message = "Sale transaction saved!"
    success_url = reverse_lazy('sales:add')

class SaleListView(ListView):
    model = Sale
    queryset = Sale.objects.order_by('-purchase_date')
    template_name = 'sales/transactions.html'
    context_object_name = 'sales'

class SaleUpdateView(UpdateView):
    model = Sale
    template_name = 'sales/edit_sale_form.html'
    form_class = SaleForm
    success_url = reverse_lazy('sales:transactions')


def delete_sale(request, pk):
    sale = get_object_or_404(Sale, id=pk)
    sale.delete()
    return redirect(reverse('sales:transactions'))

def load_items(request):
    category_id = request.GET['category']
    items = Item.objects.filter(category_id=category_id).order_by('item')
    return render(request, 'sales/item_options.html', context={'items': items})