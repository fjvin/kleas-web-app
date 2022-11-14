from django.db import models
from django.core.validators import MinValueValidator, DecimalValidator, MaxValueValidator
from sales import models as sales_models

# Create your models here.

# expenses-restock table
class ExpensesRestock(models.Model):
    price = models.DecimalField(max_digits=9, decimal_places=2, 
                                validators=[
                                    MinValueValidator(limit_value=1.00),
                                    MaxValueValidator(limit_value=1000000.00),
                                    DecimalValidator(max_digits=9, decimal_places=2)])

    quantity = models.IntegerField(validators=[MinValueValidator(limit_value=1)])
    purchase_date = models.DateTimeField(auto_now_add=True)

    PAYMENT_TYPE = (
        ('cash', 'Cash'),
        ('cashless', 'Cashless')
    )
    payment = models.CharField(max_length=10, choices=PAYMENT_TYPE)
    category = models.ForeignKey(sales_models.Category, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(sales_models.Item, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.category}-{self.item}"

# expenses-store table
class ExpensesStore(models.Model):
    amount = models.DecimalField(max_digits=9, decimal_places=2,
                                validators=[
                                    MinValueValidator(limit_value=1.00),
                                    MaxValueValidator(limit_value=1000000.00),
                                    DecimalValidator(max_digits=9, decimal_places=2)])
    date = models.DateField()

    CATEGORY = [
        ('Utilities', (
                ('electricity', 'Electricity'),
                ('water', 'Water'),
            )
        ),
        ('tax', ' Tax'),
        ('lease', 'Lease')
    ]
    category = models.CharField(max_length=20, choices=CATEGORY)

    def __str__(self):
        return self.category