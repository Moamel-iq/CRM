# Generated by Django 4.2.7 on 2023-11-01 09:20

from django.db import migrations, models
import django.utils.timezone
import django_countries.fields
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0002_alter_account_billing_country_alter_account_country_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('customer_name', models.CharField(db_index=True, max_length=200)),
                ('customer_email', models.EmailField(max_length=254)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=200)),
                ('customer_address', models.CharField(max_length=200)),
                ('mobile_no', phonenumber_field.modelfields.PhoneNumberField(default='+8801', max_length=128, region=None)),
                ('city', django_countries.fields.CountryField(default='BD', max_length=2)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('previous_balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.DeleteModel(
            name='Account',
        ),
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['customer_name'], name='hr_customer_custome_0b0cfd_idx'),
        ),
    ]
