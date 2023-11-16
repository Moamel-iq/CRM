from home.views import Dashboard
from django.urls import path, include

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),

]
