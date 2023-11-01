# Generated by Django 4.2.7 on 2023-11-01 23:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0003_categoryexpense_order_stock_service_return_purchase_and_more'),
        ('hr', '0006_bank_signature_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceTrack',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('user_agent', models.CharField(blank=True, help_text='e.g. Chrome 98, Windows, TECNO KE5, Android', max_length=255, null=True, verbose_name='User Agent')),
                ('last_activity', models.DateTimeField(blank=True, help_text='Last activity of the device', null=True, verbose_name='Last Activity')),
                ('ip_address', models.GenericIPAddressField(blank=True, default='', help_text='IP address of the device', null=True, verbose_name='IP Address')),
                ('location', models.CharField(blank=True, help_text='Location of the device', max_length=255, null=True, verbose_name='Location')),
                ('timezone', models.CharField(blank=True, max_length=255, null=True, verbose_name='Timezone')),
            ],
            options={
                'verbose_name': 'Device Activity',
                'verbose_name_plural': 'Device Activity',
                'ordering': ('-last_activity',),
            },
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('windows', models.IntegerField(default=0)),
                ('mac', models.IntegerField(default=0)),
                ('linux', models.IntegerField(default=0)),
                ('android', models.IntegerField(default=0)),
                ('ios', models.IntegerField(default=0)),
                ('other', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Visitor',
                'verbose_name_plural': 'Visitors',
            },
        ),
        migrations.CreateModel(
            name='SalesAnalytics',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('sales_volume', models.PositiveIntegerField()),
                ('revenue', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InventoryAnalytics',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('stock_level', models.PositiveIntegerField()),
                ('stockout_count', models.PositiveIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerAnalytics',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('total_orders', models.PositiveIntegerField()),
                ('total_spent', models.DecimalField(decimal_places=2, max_digits=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.customer')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
