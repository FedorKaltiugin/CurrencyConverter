# Generated by Django 4.2.14 on 2024-07-13 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("converter", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="currencyconverter",
            name="created_date",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Created Date"),
        ),
        migrations.AlterField(
            model_name="currencyconverter",
            name="currency",
            field=models.CharField(
                choices=[("CZK", "Czech koruna"), ("EUR", "Euro"), ("PLN", "Polish zloty"), ("USD", "US dollar")],
                max_length=3,
                verbose_name="Short Name",
            ),
        ),
        migrations.AlterField(
            model_name="currencyconverter",
            name="updated_date",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated Date"),
        ),
    ]
