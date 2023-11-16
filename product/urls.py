from django.urls import path

from product.views.sale.sales import SalesList
from product.views.expense.manage_expense import ManageExpense

app_name = 'product'

urlpatterns = [
    path('', SalesList.as_view(), name='sales_list'),
    path('expense/', ManageExpense.as_view(), name='manage_expense'),

    ]