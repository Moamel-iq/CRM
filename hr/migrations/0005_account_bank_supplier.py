# Generated by Django 4.2.7 on 2023-11-01 16:15

from django.db import migrations, models
import django.utils.timezone
import django_countries.fields
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0004_alter_customer_city_alter_customer_mobile_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=25, verbose_name='Name of Account')),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(default='+964', max_length=128, region='IQ', verbose_name='Phone Number')),
                ('industry', models.CharField(blank=True, choices=[('ADVERTISING', 'ADVERTISING'), ('AGRICULTURE', 'AGRICULTURE'), ('APPAREL & ACCESSORIES', 'APPAREL & ACCESSORIES'), ('AUTOMOTIVE', 'AUTOMOTIVE'), ('BANKING', 'BANKING'), ('BIOTECHNOLOGY', 'BIOTECHNOLOGY'), ('BUILDING MATERIALS & EQUIPMENT', 'BUILDING MATERIALS & EQUIPMENT'), ('CHEMICAL', 'CHEMICAL'), ('COMPUTER', 'COMPUTER'), ('EDUCATION', 'EDUCATION'), ('ELECTRONICS', 'ELECTRONICS'), ('ENERGY', 'ENERGY'), ('ENTERTAINMENT & LEISURE', 'ENTERTAINMENT & LEISURE'), ('FINANCE', 'FINANCE'), ('FOOD & BEVERAGE', 'FOOD & BEVERAGE'), ('GROCERY', 'GROCERY'), ('HEALTHCARE', 'HEALTHCARE'), ('INSURANCE', 'INSURANCE'), ('LEGAL', 'LEGAL'), ('MANUFACTURING', 'MANUFACTURING'), ('PUBLISHING', 'PUBLISHING'), ('REAL ESTATE', 'REAL ESTATE'), ('SERVICE', 'SERVICE'), ('SOFTWARE', 'SOFTWARE'), ('SPORTS', 'SPORTS'), ('TECHNOLOGY', 'TECHNOLOGY'), ('TELECOMMUNICATIONS', 'TELECOMMUNICATIONS'), ('TELEVISION', 'TELEVISION'), ('TRANSPORTATION', 'TRANSPORTATION'), ('VENTURE CAPITAL', 'VENTURE CAPITAL')], help_text='Industry Type: ', max_length=255, null=True)),
                ('country', django_countries.fields.CountryField(default='IQ', max_length=2, verbose_name='Country')),
                ('divistion', models.CharField(blank=True, choices=[('dhaka', 'Dhaka'), ('sylhet', 'Sylhet'), ('barishal', 'Barishal'), ('chattogram', 'Chattogram'), ('khulna', 'Khulna'), ('rajshahi', 'Rajshahi'), ('rangpur', 'Rangpur'), ('mymensingh', 'Mymensingh')], max_length=25, null=True, verbose_name='Division')),
                ('districts', models.CharField(blank=True, choices=[('dhaka', 'Dhaka'), ('faridpur', 'Faridpur'), ('gazipur', 'Gazipur'), ('gopalganj', 'Gopalganj'), ('jamalpur', 'Jamalpur'), ('kishoreganj', 'Kishoreganj'), ('madaripur', 'Madaripur'), ('manikganj', 'Manikganj'), ('munshiganj', 'Munshiganj'), ('narayanganj', 'Narayanganj'), ('narsingdi', 'Narsingdi'), ('netrokona', 'Netrokona'), ('rajbari', 'Rajbari'), ('shariatpur', 'Shariatpur'), ('sherpur', 'Sherpur'), ('tangail', 'Tangail'), ('bogra', 'Bogra'), ('joypurhat', 'Joypurhat'), ('naogaon', 'Naogaon'), ('natore', 'Natore'), ('nawabganj', 'Nawabganj'), ('pabna', 'Pabna'), ('rajshahi', 'Rajshahi'), ('sirajganj', 'Sirajganj'), ('dinajpur', 'Dinajpur'), ('gaibandha', 'Gaibandha'), ('kurigram', 'Kurigram'), ('lalmonirhat', 'Lalmonirhat'), ('nilphamari', 'Nilphamari'), ('panchagarh', 'Panchagarh'), ('rangpur', 'Rangpur'), ('thakurgaon', 'Thakurgaon'), ('barguna', 'Barguna'), ('barisal', 'Barisal'), ('bhola', 'Bhola'), ('jhalokati', 'Jhalokati'), ('patuakhali', 'Patuakhali'), ('pirojpur', 'Pirojpur'), ('bandarban', 'Bandarban'), ('brahmanbaria', 'Brahmanbaria'), ('chandpur', 'Chandpur'), ('chittagong', 'Chittagong'), ('comilla', 'Comilla'), ("cox's bazar", "Cox's bazar"), ('feni', 'Feni'), ('khagrachhari', 'Khagrachhari'), ('lakshmipur', 'Lakshmipur'), ('noakhali', 'Noakhali'), ('rangamati', 'Rangamati'), ('habiganj', 'Habiganj'), ('moulvibazar', 'Moulvibazar'), ('sunamganj', 'Sunamganj'), ('sylhet', 'Sylhet'), ('bagerhat', 'Bagerhat'), ('chuadanga', 'Chuadanga'), ('jessore', 'Jessore'), ('jhenaidah', 'Jhenaidah'), ('khulna', 'Khulna'), ('kushtia', 'Kushtia'), ('magura', 'Magura'), ('meherpur', 'Meherpur'), ('narail', 'Narail'), ('satkhira', 'Satkhira')], max_length=25, null=True, verbose_name='District')),
                ('billing_address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address')),
                ('billing_street', models.CharField(blank=True, max_length=255, null=True, verbose_name='Street')),
                ('billing_city', models.CharField(blank=True, max_length=255, null=True, verbose_name='City')),
                ('billing_state', models.CharField(blank=True, max_length=255, null=True, verbose_name='State')),
                ('billing_postcode', models.CharField(blank=True, max_length=255, null=True, verbose_name='Post/Zip-code')),
                ('billing_country', django_countries.fields.CountryField(default='IQ', max_length=2, verbose_name='Country')),
                ('status', models.CharField(choices=[('open', 'Open'), ('close', 'Close')], default='open', max_length=64)),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
            },
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('bank_account_name', models.CharField(max_length=25, verbose_name='A/C Name')),
                ('bank_name', models.CharField(max_length=25, verbose_name='Bank Name')),
                ('bank_short_name', models.CharField(blank=True, max_length=5, null=True, verbose_name='Bank Short Name')),
                ('bank_account_number', models.IntegerField(unique=True, verbose_name='A/C Number')),
                ('bank_branch', models.CharField(max_length=25, verbose_name='Branch')),
                ('account_type', models.CharField(choices=[('savings account', 'Savings Account'), ('current account', 'Current Account'), ('fixed Deposit account', 'Fixed Deposit Account'), ('recurring Deposit account', 'Recurring Deposit Account')], max_length=225, verbose_name='Bank Account Type')),
            ],
            options={
                'verbose_name': 'Bank',
                'verbose_name_plural': 'Bank',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('supplier_full_name', models.CharField(max_length=100, verbose_name='Supplier Full Name')),
                ('supplier_address', models.CharField(max_length=100, verbose_name='Supplier Address')),
                ('supplier_phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('supplier_email', models.EmailField(max_length=254, unique=True, verbose_name='Supplier Email')),
                ('supplier_zip_code', models.CharField(max_length=10)),
                ('supplier_country', django_countries.fields.CountryField(max_length=2)),
                ('supplier_fax', models.BigIntegerField(blank=True, null=True, verbose_name='Supplier Fax')),
                ('supplier_previous_balance', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Supplier Previous Balance')),
            ],
            options={
                'verbose_name': 'Supplier',
                'verbose_name_plural': 'Suppliers',
            },
        ),
    ]
