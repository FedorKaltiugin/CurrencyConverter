from rest_framework import serializers

from converter.models import CurrencyConverter


class CurrencyConverterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyConverter
        fields = ("currency", "cur_to_usd")
