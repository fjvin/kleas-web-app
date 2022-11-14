from django.db import models
from django.core.validators import MinValueValidator, DecimalValidator, MaxValueValidator

# clothes category table
class Category(models.Model):
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.category

# clothes item category table
class Item(models.Model):
    item = models.CharField(max_length=20)
    category = models.ForeignKey(Category, 
                                on_delete=models.CASCADE, 
                                related_name="categories")

    def __str__(self):
        return self.item


# sale transactions table
class Sale(models.Model):
    price = models.DecimalField(max_digits=9, 
                                decimal_places=2, 
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

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.category}-{self.item}"