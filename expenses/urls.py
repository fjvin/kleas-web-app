from django.urls import path
from . import views

app_name = "expenses"

urlpatterns = [
    path("", views.restock, name="restock"),
    path("store/", views.store, name="store"),
]
