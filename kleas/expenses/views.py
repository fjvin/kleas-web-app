from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages

from . models import ExpensesRestock, ExpensesStore
from . forms import ExpensesRestockForm, ExpensesStoreForm

# Expenses Restock Views
class ExpensesRestockCreateView(SuccessMessageMixin, CreateView):
    model = ExpensesRestock
    form_class = ExpensesRestockForm
    template_name = 'expenses/expenses_restock/restock_form.html'
    success_message = "Expense transaction saved!"
    success_url = reverse_lazy('expenses:restock')

class ExpensesRestockListView(ListView):
    model = ExpensesRestock
    queryset = ExpensesRestock.objects.order_by('-purchase_date')
    template_name = 'expenses/expenses_restock/transactions.html'
    context_object_name = 'expenses'

class ExpensesRestockUpdateView(SuccessMessageMixin, UpdateView):
    model = ExpensesRestock
    template_name = 'expenses/expenses_restock/edit_restock_form.html'
    form_class = ExpensesRestockForm
    success_message = "Expense transaction updated!"
    success_url = reverse_lazy('expenses:restock_transactions')

def delete_restock(request, pk):
    expense = get_object_or_404(ExpensesRestock, id=pk)
    expense.delete()
    messages.success(request, 'Expense transaction deleted!')
    return redirect(reverse('expenses:restock_transactions'))

##################################################################

# Expenses Store Views
class ExpensesStoreCreateView(SuccessMessageMixin, CreateView):
    model = ExpensesStore
    form_class = ExpensesStoreForm
    template_name = 'expenses/expenses_store/store_form.html'
    success_message = "Expense transaction saved!"
    success_url = reverse_lazy('expenses:store')

class ExpensesStoreListView(ListView):
    model = ExpensesStore
    queryset = ExpensesStore.objects.order_by('-date')
    template_name = 'expenses/expenses_store/transactions.html'
    context_object_name = 'expenses'

class ExpensesStoreUpdateView(SuccessMessageMixin, UpdateView):
    model = ExpensesStore
    template_name = 'expenses/expenses_store/edit_store_form.html'
    form_class = ExpensesStoreForm
    success_message = "Expense transaction updated!"
    success_url = reverse_lazy('expenses:store_transactions')

def delete_store(request, pk):
    expense = get_object_or_404(ExpensesStore, id=pk)
    expense.delete()
    messages.success(request, 'Expense transaction deleted!')
    return redirect(reverse('expenses:store_transactions'))