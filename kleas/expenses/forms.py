from django import forms
from .models import ExpensesRestock, ExpensesStore

class ExpensesRestockForm(forms.ModelForm):
    class Meta:
        model = ExpensesRestock
        exclude = ('purchase_date',)

        # ExpensesRestock Form HTML Widgets Reference
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

##################################################################

class DateInput(forms.DateInput):
    input_type = 'date'

class ExpensesStoreForm(forms.ModelForm):
    class Meta:
        model = ExpensesStore
        fields = '__all__'

        # ExpensesStore Form HTML Widgets Reference
        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "id": "price-num-input", 
                    "class": "form-control",
                    "value":"1.00",
                    "min":"1.00",
                    "required": True,
                    'type': 'currency',
                    }
                ),
            "date": DateInput(
                attrs={
                    'id': 'date',
                    'name': 'date',
                    'required': True
                }
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
        }