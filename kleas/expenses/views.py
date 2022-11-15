from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages

from . models import ExpensesRestock
from . forms import ExpensesRestockForm

# Create your views here.

class ExpensesRestockCreateView(SuccessMessageMixin, CreateView):
    model = ExpensesRestock
    form_class = ExpensesRestockForm
    template_name = 'expenses/expenses_restock_form.html'
    success_message = "Expense transaction saved!"
    success_url = reverse_lazy('expenses:restock')
