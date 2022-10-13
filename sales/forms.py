from django import forms
from .models import Sale, Category, Item

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('price', 'quantity', 'category', 'item')

        # Sale Form HTML Widgets Reference
        widgets = {
            "price": forms.NumberInput(
                attrs={
                    "id": "price-num-input", 
                    "class": "form-control", 
                    "value": "0.00",
                    "min":"0"}
                    ),
            "quantity": forms.NumberInput(
                attrs={
                    "id": "quantity-num-input", 
                    "class": "form-control", 
                    "value": "1"
                    }
                ),
            
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['item'].queryset = Item.objects.filter(category_id=category_id).order_by('item')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty items queryset
        elif self.instance.pk:
            self.fields['item'].queryset = self.instance.category.item_set.order_by('item')