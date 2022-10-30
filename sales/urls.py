from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    # sales/
    path('', views.add, name='add'),
    # /sales/delete_sale/<primary-key of sale to be deleted>
    path('delete_sale/<int:pk>', views.delete, name='delete_sale'),
    # /sales/transactions/
    path('transactions/', views.SaleTransactions.as_view(), name='transactions'),
    # /sales/edit_sale/<primary-key of sale to be edited>
    path('edit_sale/<int:pk>', views.edit, name='edit_sale'),
    # /sales/edit_sale/update <primary-key of sale to be updated>
    path('edit_sale/update/<int:pk>', views.update, name='update_sale'),

    # endpoint where ajax updates clothes items based on category
    path('ajax/load-items/', views.load_items, name='ajax_load_items'),
]
