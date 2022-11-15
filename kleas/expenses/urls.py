from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.ExpensesRestockCreateView.as_view(), name='restock'),
    path('update_restock/<int:pk>', views.ExpensesRestockUpdateView.as_view(), 
        name='update_restock'),
    path('delete_restock/<int:pk>', views.delete_restock, name='delete_restock'),
    path('restock_transactions/', views.ExpensesRestockListView.as_view(), 
        name='restock_transactions'),

    path('store/', views.ExpensesStoreCreateView.as_view(), name='store'),
    path('update_store/<int:pk>', views.ExpensesStoreUpdateView.as_view(), name='update_store'),
    path('store_transactions/', views.ExpensesStoreListView.as_view(), 
        name='store_transactions'),
    path('delete_store/<int:pk>', views.delete_store, name='delete_store'),
]
