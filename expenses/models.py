from unicodedata import category
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import sales

# Create your models here.

# expenses-restock table
class ExpensesRestock(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=2, 
                                validators=[MinValueValidator(limit_value=0.00)])
    quantity = models.IntegerField(validators=[MinValueValidator(limit_value=1)])
    purchase_date = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(sales.models.PaymentType, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(sales.models.Category, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(sales.models.Item, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.category}-{self.item}"

# expenses-store table
class ExpensesStore(models.Model):
    amount = models.DecimalField(max_digits=9, decimal_places=2, 
                                validators=[
                                    MinValueValidator(limit_value=0.00),
                                    MaxValueValidator(limit_value=1000000.00)])
    date = models.DateField()
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.category