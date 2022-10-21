from django.core.management.base import BaseCommand
from sales.models import Category, Item, PaymentType


class Command(BaseCommand):
    help = 'Load Clothes Categories, Items, and Payment Type'
    
    def handle(self, *args, **kwargs):
        Category.objects.all().delete()
        categories_names = [
            'Men', 'Women', 'Child Boys', 'Child Girls'
        ]

        if not Category.objects.count():
            for category_name in categories_names:
                Category.objects.create(category=category_name)

        # Men
        men = Category.objects.get(category='Men')
        men_items = [
            'polo',
            'sando',
            'short',
            't-shirt', 
            'hoodie',
        ]

        for item in men_items:
            Item.objects.create(item=item, category=men)

        # Women
        women = Category.objects.get(category='Women')
        women_items = [
            't-shirt',
            'dress',
            'crop-top',
            'blouse',
            'pants',
            'terno',
            'skirts',
            'hoodie',
        ]

        for item in women_items:
            Item.objects.create(item=item, category=women)

        # Child Boys
        child_boys = Category.objects.get(category='Child Boys')
        child_boys_items = [
            't-shirt',
            'pants',
            'terno',
        ]

        for item in child_boys_items:
            Item.objects.create(item=item, category=child_boys)

        # Child Girls
        child_girls = Category.objects.get(category='Child Girls')
        child_girls_items = [
            't-shirt',
            'pants',
            'skirts',
            'terno',
            'onesie',
            'dress',
        ]

        for item in child_girls_items:
            Item.objects.create(item=item, category=child_girls)


        PaymentType.objects.all().delete()
        payment_types = [
            'cash', 'cashless'
        ]

        if not PaymentType.objects.count():
            for payment_type in payment_types:
                PaymentType.objects.create(payment=payment_type)