from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.decorators import admin_only
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages

from . models import Sale, Item
from . forms import SaleForm


# Create your views here.
@method_decorator(decorator=admin_only, name='dispatch')
class SaleCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sales/sale_form.html'
    success_message = "Sale transaction saved!"
    success_url = reverse_lazy('sales:add')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    queryset = Sale.objects.order_by('-purchase_date')
    template_name = 'sales/transactions.html'
    context_object_name = 'sales'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

@method_decorator(decorator=admin_only, name='dispatch')
class SaleUpdateView(LoginRequiredMixin, UpdateView):
    model = Sale
    template_name = 'sales/edit_sale_form.html'
    form_class = SaleForm
    success_message = "Sale transaction updated!"
    success_url = reverse_lazy('sales:transactions')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

@login_required
@admin_only
def delete_sale(request, pk):
    sale = get_object_or_404(Sale, id=pk)
    sale.delete()
    messages.success(request, 'Sale transaction deleted!')
    return redirect(reverse('sales:transactions'))

@login_required
@admin_only
def load_items(request):
    category_id = request.GET['category']
    items = Item.objects.filter(category_id=category_id).order_by('item')
    return render(request, 'sales/item_options.html', context={'items': items})