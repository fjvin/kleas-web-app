from django.urls import path
from . import views

app_name = "sales"

urlpatterns = [
    path("", views.add, name="add"),
    path("transactions/", views.SaleTransactions.as_view(), name="transactions"),
    path("edit_sale/<int:pk>", views.SaleEdit.as_view(), name="edit_sale"),
    path("delete_sale/<int:pk>", views.SaleDelete.as_view(), name="delete_sale"),

    path('ajax/load-items/', views.load_items, name='ajax_load_items'),
]
