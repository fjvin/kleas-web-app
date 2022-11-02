from django.shortcuts import render, redirect
from django.contrib import messages 
from django.urls import reverse
from .models import ExpensesRestock, ExpensesStore
from sales.models import PaymentType, Category, Item
from django.contrib.auth.decorators import login_required


@login_required
def transactions_store(request):
    store_expenses = ExpensesStore.objects.all()
    context = {
        'store_expenses': store_expenses,
        }
    return render(request, 'expenses/store_transactions.html', context=context)

@login_required
def transactions_restock(request):
    restock_expenses = ExpensesRestock.objects.all()
    context = {
        'restock_expenses': restock_expenses,
        }
    return render(request, 'expenses/restock_transactions.html', context=context)

# add restock expenses
@login_required
def restock(request):

    # check if request is POST, if yes, save the expense
    if request.method == 'POST':
        restockObj = ExpensesRestock()
        restockObj.price = request.POST['price']
        restockObj.quantity = request.POST['quantity']
        restockObj.payment = PaymentType.objects.get(id=request.POST['payment'])
        restockObj.category = Category.objects.get(id=request.POST['category'])
        restockObj.item = Item.objects.get(id=request.POST['item'])
        restockObj.save()
        messages.success(request, 'Restock-Expense Saved!')
        return redirect(reverse('expenses:restock'))
    # else render empty form
    else:
        return render(request, 'expenses/restock.html')

# edit restock record
@login_required
def edit_restock(request, pk):
    expense = ExpensesRestock.objects.get(id=pk)
    context = {
        'expense': expense,
    }
    return render(request, 'expenses/restock_edit.html', context=context)

# update restock record
@login_required
def update_restock(request, pk):
    expense = ExpensesRestock.objects.get(id=pk)
    expense.price = request.POST['price']
    expense.quantity = request.POST['quantity']
    expense.payment = PaymentType.objects.get(id=request.POST['payment'])
    expense.category = Category.objects.get(id=request.POST['category'])
    expense.item = Item.objects.get(id=request.POST['item'])
    expense.save()
    return redirect(reverse('expenses:transactions_restock'))

# edit store record
@login_required
def edit_store(request, pk):
    expense = ExpensesStore.objects.get(id=pk)
    context = {
        'expense': expense,
    }
    return render(request, 'expenses/store_edit.html', context=context)

# update store record
@login_required
def update_store(request, pk):
    expense = ExpensesStore.objects.get(id=pk)
    expense.amount = request.POST['amount']
    expense.date = request.POST['date']
    expense.category = request.POST['category']
    expense.save()
    return redirect(reverse('expenses:transactions_store'))

# delete restock expenses function-based view
@login_required
def delete_restock(request, pk):
    expense = ExpensesRestock.objects.get(id=pk)
    expense.delete()
    return redirect(reverse('expenses:transactions_restock'))

# delete store expenses function-based view
@login_required
def delete_store(request, pk):
    expense = ExpensesStore.objects.get(id=pk)
    expense.delete()
    return redirect(reverse('expenses:transactions_store'))

# add store expense
@login_required
def store(request):
    # check if request is POST, if yes, save the expense
    if request.method == 'POST':
        expense = ExpensesStore()
        expense.amount = request.POST['amount']
        expense.date = request.POST['date']
        expense.category = request.POST['category']
        expense.save()
        messages.success(request, 'Store-Expense Saved!')
        return redirect(reverse('expenses:store'))
    # else render the form
    else:
        return render(request, 'expenses/store.html')