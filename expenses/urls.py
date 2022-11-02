from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    # expenses/
    path('', views.restock, name='restock'),
    # expenses/store
    path('store/', views.store, name='store'),

    # expenses/transactions/restock
    path('transactions/restock', views.transactions_restock, name='transactions_restock'),
    # expenses/transactions/store
    path('transactions/store', views.transactions_store, name='transactions_store'),

    # expenses/edit_restock/<primary-key of restock expense to be edit>
    path('edit_restock/<int:pk>', views.edit_restock, name='edit_restock'),
    # expenses/edit/update/<primary-key of restock to be update>
    path('edit_restock/update/<int:pk>', views.update_restock, name='update_restock'),

    # expenses/edit_store/<primary-key of store expense to be edit>
    path('edit_store/<int:pk>', views.edit_store, name='edit_store'),
    # expenses/edit_store/update/<primary-key of store expense to be update>
    path('edit_store/update/<int:pk>', views.update_store, name='update_store'),

    # /expenses/delete_restock/<primary-key of restock expense to be deleted>
    path('delete_restock/<int:pk>', views.delete_restock, name='delete_restock'),
     # /expenses/delete_store/<primary-key of restock expense to be deleted>
    path('delete_store/<int:pk>', views.delete_store, name='delete_store'),
]
