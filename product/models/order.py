from hr.models import Customer
from django.db import models
from product.models.product import Product
from abstract.utils.models import Timestamp

class Order(Timestamp):
    """
    Damage model for storing order history🛢
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=[('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default=[('processing', 'Processing')])
    quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """String for representing the Model object."""
        return self.status
