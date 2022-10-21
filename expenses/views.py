from django.shortcuts import render, redirect
from django.contrib import messages 
from django.urls import reverse
from .models import ExpensesRestock, ExpensesStore
from sales.models import PaymentType, Category, Item


# Create your views here.
def restock(request):
    if request.method == "POST":
        restockObj = ExpensesRestock()
        restockObj.price = request.POST["price"]
        restockObj.quantity = request.POST["quantity"]
        restockObj.payment = PaymentType.objects.get(id=request.POST["payment"])
        restockObj.category = Category.objects.get(id=request.POST["category"])
        restockObj.item = Item.objects.get(id=request.POST["item"])
        restockObj.save()

        messages.success(request, "Restock-Expense Saved!")

        return redirect(reverse("expenses:restock"))
    else:
        return render(request, "expenses/restock.html")


def store(request):
    if request.method == "POST":
        expense = ExpensesStore()
        expense.amount = request.POST["amount"]
        expense.date = request.POST["date"]
        expense.category = request.POST["category"]
        expense.save()

        messages.success(request, "Store-Expense Saved!")

        return redirect(reverse("expenses:store"))
    else:
        return render(request, "expenses/store.html")