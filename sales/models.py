from django.db import models
from django.core.validators import MinValueValidator

# clothes category table
class Category(models.Model):
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.category

# clothes item category table
class Item(models.Model):
    item = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return self.item

# payment type table
class PaymentType(models.Model):
    payment = models.CharField(max_length=20)

    def __str__(self):
        return self.payment

# sale transactions table
class Sale(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=2, 
                                validators=[MinValueValidator(limit_value=0.00)])
    quantity = models.IntegerField(validators=[MinValueValidator(limit_value=1)])
    purchase_date = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(PaymentType, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.category}-{self.item}"