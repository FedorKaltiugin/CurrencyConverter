from django.contrib import admin

from converter.models import CurrencyConverter


@admin.register(CurrencyConverter)
class Adminaa(admin.ModelAdmin):
    fields = ("currency", "cur_to_usd")
