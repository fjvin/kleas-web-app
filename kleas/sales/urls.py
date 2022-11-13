from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.SaleCreateView.as_view(), name='add'),
    path('transactions/', views.SaleListView.as_view(), name='transactions'),
    path('update_sale/<int:pk>', views.SaleUpdateView.as_view(), name='update_sale'),

    # endpoint where ajax updates clothes items based on category
    path('ajax/load-items/', views.load_items, name='ajax_load_items'),
]
