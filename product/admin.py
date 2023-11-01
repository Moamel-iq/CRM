import json

from import_export.admin import ImportExportModelAdmin
from decimal import Decimal
from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.utils.html import format_html
from .models import Damage, Expense, Order, Purchase, Return, Service, Stock
from .models.expense import CategoryExpense
from .models.product import Category, Product, Unit
from .models.sales import Sale


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = (
        'product_name',
        'product_code',
        'price',
        'quantity',
        'supplier_price',
        'unit',
        'category',
        'in_stock',
        '_status',
        'supplier',

    )
    list_filter = ('status', 'category', 'unit', 'status', 'supplier')
    search_fields = ('name', 'category__name', 'unit__name')
    list_per_page = 20
    list_editable = ('quantity', 'price')

    fieldsets = (
        (None, {
            "fields": (
                'product_name', 'brand_name', 'manufacturer', 'product_description', 'image', 'in_stock', 'country',
            ),
        }),
        ('Price', {
            'fields': ('price', 'supplier_price')
        }),
        ('Unit', {
            'fields': ('unit',)
        }),
        ('Category', {
            "fields": ('category',),
        }),
        ('Mfg. Date', {
            "fields": ('mfg_date',),
        }),
        ('Exp. Date', {
            "fields": ('exp_date',),
        }),
        ('Barcode and QR Code', {
            'classes': ('collapse',),
            'fields': ('barcode', 'qrcode')
        }),
        ('Supplier', {
            "fields": ('supplier',),
        }),
        ('Other Details', {
            'classes': ('collapse',),
            'fields': (
                'size', 'color', 'weight', 'height', 'shape', 'material_type',
                'hard_disk_size', 'screen_size', 'operating_system', 'cpu_manufacturer',
                'connectivity_technology', 'uses_for_product')
        }),

    )

    def _status(self, obj):
        '''
        This method is used to display the status of the product status in colord text.
        '''
        if obj.out_of_stock is False:
            return format_html('<span style="color: #008000; font-weight: bold;">In Stock</span>')
        elif obj.out_of_stock is True:
            return format_html('<span style="color:#DC143C; font-weight: bold;">Out Of Stock</span>')
        else:
            return obj.status


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    list_per_page = 10


@admin.register(Unit)
class UnitAdmin(ImportExportModelAdmin):
    list_display = ('name', 'status')
    list_filter = ('status',)
    search_fields = ('name',)
    list_per_page = 10


@admin.register(Damage)
class DamageAdmin(ImportExportModelAdmin):
    list_display = ('product', 'damaged_date', 'damaged_reason', 'customer', 'supplier')


@admin.register(Expense)
class ExpenseAdmin(ImportExportModelAdmin):
    list_display = ('date', 'expense_type', 'amount', 'category')


@admin.register(CategoryExpense)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('name',)


@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    list_display = ('customer', 'order_date', 'status', 'total_amount')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    date_hierarchy = 'purchase_date'
    list_display = (
        'product', 'supplier', 'invoice_number',
        'purchase_id', 'purchase_date', 'payment_method',
        'discount', 'paid_amount', 'due_amount', 'total_amount'
    )
    list_filter = ('purchase_date', 'payment_method')
    fieldsets = (
        (None, {
            'fields': ('product', 'supplier', 'purchase_date', 'payment_method', 'details',
                       'discount', 'paid_amount', 'due_amount', 'total_amount')
        }),
    )
    readonly_fields = ('invoice_number', 'purchase_id',)
    search_fields = ('invoice_number', 'purchase_id',)
    ordering = ('-purchase_date',)
    list_per_page = 10
    exclude = ('invoice_number', 'purchase_id',)
    list_editable = ('paid_amount', 'due_amount',)

    def save_model(self, request, obj, form, change):
        '''
        Associate model with current user while saving.
        '''
        obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Return)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        '_invoice_number', 'customer', 'product',
        'date', 'payment_method', '_status', 'is_paid',
        'due', 'total'
    )
    actions = ('discount_30',)
    list_filter = ('status', 'date', 'payment_method', 'product', 'customer',)
    exclude = ('user', 'status', 'invoice_number')

    def discount_30(self, request, queryset):
        from math import ceil
        discount = 30  # percentage

        for sale in queryset:
            ''' Set a discount of 30% to selected sales '''
            multiplier = discount / 100
            old_price = sale.total
            discounted_price = ceil(old_price - (old_price * Decimal(multiplier)))
            sale.total = discounted_price
            sale.save(update_fields=['total'])

    discount_30.short_description = 'Set 30%% discount'

    def _status(self, obj):
        '''
        Return the status of the sale colorized in red or green depending on the status.
        '''
        return format_html('<span style="color:green">✅Paid</span>') if obj.is_paid else format_html(
            '<span style="color:red">⌛Due</span>')

    def _invoice_number(self, obj):
        '''
        Return the invoice_number colorized in admin.
        '''
        return format_html('<span style="color:green;">#{}</span>', obj.invoice_number)

    def save_model(self, request, obj, form, change):
        '''
        Associate model with current user while saving.
        '''
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        ''' Aggregate new customers per day '''
        chart_data = (
            Sale.objects.annotate(date=TruncDay("created_at")).values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)

        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('customer', 'service_name', 'description', 'charge')
    search_fields = ('service_name',)
    list_filter = ('customer',)
    ordering = ('customer',)

    def save_model(self, request, obj, form, change):
        '''
        Associate model with current user while saving.
        '''
        obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Stock)
