from django import forms
from .models import Sale

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        exclude = ('purchase_date',)

        # Sale Form HTML Widgets Reference
        widgets = {
            "price": forms.NumberInput(
                attrs={
                    "id": "price-num-input", 
                    "class": "form-control",
                    "value":"1.00",
                    "min":"1.00",
                    "required": True,
                    'type': 'currency',
                    }
                ),
            "quantity": forms.NumberInput(
                attrs={
                    "id": "quantity-num-input", 
                    "class": "form-control", 
                    "min":"1",
                    "value": "1",
                    "required": True
                }
            ),
            "payment": forms.Select(
                attrs={
                    "id": "payment-dropdown",
                    "class": "selectpicker show-tick form-control",
                    "title":"Select Payment",
                    "data-width": "100%",
                    "data-style" :"btn-outline-primary",
                    "required": True
                },
            ),

            "category": forms.Select(
                attrs={
                    "id": "category-dropdown",
                    "class": "selectpicker show-tick form-control",
                    "title":"Select Category",
                    "data-width": "100%",
                    "data-style" :"btn-outline-primary",
                    "required": True
                },
            ),
            "item": forms.Select(
                attrs={
                    "id": "item-dropdown",
                    "class": "selectpicker show-tick form-control",
                    "title":"Select Item",
                    "data-width": "100%",
                    "data-style" :"btn-outline-primary",
                    "required": True
                },
            ),
        }