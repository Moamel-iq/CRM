from django.db import models
from abstract.utils.models import Timestamp


class CategoryExpense(Timestamp):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category Expense'
        verbose_name_plural = 'Categories Expense'


class Expense(Timestamp):
    """
    Expense model for storing expense data🛢
    """
    date = models.DateField(auto_now_add=True)
    expense_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(CategoryExpense, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return f"{self.expense_type} - {self.amount}"
