from django.urls import path
from . import views

app_name = "sales"

urlpatterns = [
    path("", views.add, name="add"),
    path("transactions/", views.SaleTransactions.as_view(), name="transactions"),
    path("success/", views.success, name="success"),

    path('ajax/load-items/', views.load_items, name='ajax_load_items'),
]
