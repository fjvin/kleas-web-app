from django.views.generic import CreateView
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


def load_items(request):
    category_id = request.GET['category']
    items = Item.objects.filter(category_id=category_id).order_by('item')
    return render(request, 'sales/item_options.html', context={'items': items})