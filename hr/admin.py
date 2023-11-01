import json

from num2words import num2words

from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.utils.html import format_html

from .models import Bank, Supplier
from .models.customer import Customer
from account.models import User
from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'business_manager_name',
                    'is_superuser', 'is_staff', '_brand_logo', 'change', 'history')
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'is_verified')
    search_fields = ('email', )
    ordering = ('email', )
    readonly_fields = ('token',)

    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'phone_number', 'organization_name', 'business')
        }),
        ('Brand Logo™', {
            'classes': ('collapse',),
            'fields': ('brand_logo', 'defaultURL')
        }),
        ('Timestamps⏳', {
            'classes': ('collapse',),
            'fields': ('date_joined', 'password_changes_datatime', 'last_activity'),
            'description': 'Timestamps fields are automatically updated by the system.'
        }),
        ('Permissions🔐', {
            'classes': ('collapse',),
            'fields': (
                ('is_verified', 'is_superuser', 'is_active', ),
                ('is_staff', 'is_founder', 'is_ceo', 'is_manager',),
                ('is_employee', 'is_customer', 'is_supplier'),
                ('is_hr', 'is_accountant'),
            ),
            'description': 'Note: If you want to change the permissions of a user, you need to contact in our headquarters.'
        }),
        ('Session🛢', {
            'classes': ('collapse',),
            'fields': ('session',)
        }),
        ('Secret🔐', {
            'classes': ('collapse',),
            'fields': ('token',)
        }),
        ('Groups🏷', {
            'classes': ('collapse',),
            'fields': ('groups',)
        }),
    )

    def _brand_logo(self, obj):
        return format_html('<img src="{}" width="40" height="40"  loading=lazy /> '.format(obj.brand_logo))

    def change(self, obj):
        view_name = "admin:{}_{}_change".format(obj._meta.app_label, obj._meta.model_name)
        link = reverse(view_name, args=[obj.pk])
        html = '<input type="button" onclick="location.href=\'{}\'" value="Change" />'.format(link)
        return format_html(html)

    def history(self, obj):
        view_name = "admin:{}_{}_history".format(obj._meta.app_label, obj._meta.model_name)
        link = reverse(view_name, args=[obj.pk])
        html = '<input type="button" onclick="location.href=\'{}\'" value="History" />'.format(link)
        return format_html(html)


# Note: Unregister the default admin group
admin.site.unregister(Group)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('customer_name', 'gender', 'customer_email', 'mobile_no', 'customer_address', 'city', 'total')
    list_filter = ('gender', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('customer_name', 'gender', 'customer_address', 'city', 'mobile_no', 'customer_email')
        }),

        ('Payment options', {
            'classes': ('collapse',),
            'fields': ('balance', 'previous_balance')
        })
    )

    list_per_page = 10

    @admin.display(empty_value='Not Available')
    def total(self, obj):
        result = obj.balance + obj.previous_balance
        return format_html("<b>{}</b> <br> {}", result, num2words(result).capitalize())

    def changelist_view(self, request, extra_context=None):
        ''' Aggregate new customers per day '''
        chart_data = (
            Customer.objects.annotate(date=TruncDay("created_at")).values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)

        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        '''
        Associate model with current user while saving.
        '''
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('bank_account_name', 'bank_account_number', 'account_type', 'bank_name', 'bank_short_name', 'bank_branch')
    search_fields = ('bank_account_name', 'bank_account_number')
    list_filter = ('account_type', 'bank_name', 'bank_short_name', 'bank_branch')
    list_per_page = 10
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        '''
        Associate model with current user while saving.
        '''
        obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Supplier)

