from django.db import models


class CurrencyConverter(models.Model):
    class Currency(models.TextChoices):
        CZK = "CZK", "Czech koruna"
        EUR = "EUR", "Euro"
        PLN = "PLN", "Polish zloty"
        USD = "USD", "US dollar"

    currency = models.CharField(max_length=3, choices=Currency.choices, verbose_name="Short Name")
    cur_to_usd = models.FloatField(verbose_name="Rate To USD")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name = "Rate To USD"
        verbose_name_plural = "Rates To USD"
