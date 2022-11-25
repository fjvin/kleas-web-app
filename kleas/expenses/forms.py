from django import forms
from .models import ExpensesRestock, ExpensesStore
from sales.models import Item

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

    def __init__(self, *args, **kwargs):

        # remove the ":" suffix in field names
        kwargs["label_suffix"] = ""

        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.none()

        # remove the default "-------" in select fields
        payment_choices = list(self.fields["payment"].choices)[1:]
        category_choices = list(self.fields["category"].choices)[1:]
        item_choices = list(self.fields["item"].choices)[1:]

        self.fields["payment"].choices = payment_choices
        self.fields["category"].choices = category_choices
        self.fields["item"].choices = item_choices

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))  # type: ignore
                self.fields['item'].queryset = Item.objects.filter(category_id=category_id).order_by('item')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty items queryset
        elif self.instance.pk:
            self.fields['item'].queryset = self.instance.category.item_set.order_by('item')

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

    def __init__(self, *args, **kwargs):

        # remove the ":" suffix in field names
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
        # remove the default "-------" in select fields
        category_choices = list(self.fields["category"].choices)[1:]
        self.fields["category"].choices = category_choices