from django.contrib import admin

from hr.models import Account


# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country', 'industry')
    list_filter = ('industry',)
