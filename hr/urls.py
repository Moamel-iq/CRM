from django.urls import path

from hr.views.customer import CustomerList
from hr.views.supplier import SupplierList

app_name = 'hr'

urlpatterns = [
    path('customers/', CustomerList.as_view(), name='customer_list'),
    path('supplier/', SupplierList.as_view(), name='supplier_list'),
    ]