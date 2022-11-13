from django.views.generic import CreateView, ListView, UpdateView
from django.shortcuts import render
from django.urls import reverse_lazy

from . models import Sale, Item
from . forms import SaleForm

# Create your views here.

class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sales/sale_form.html'
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

def load_items(request):
    category_id = request.GET['category']
    items = Item.objects.filter(category_id=category_id).order_by('item')
    return render(request, 'sales/item_options.html', context={'items': items})