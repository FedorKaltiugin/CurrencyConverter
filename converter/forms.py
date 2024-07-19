from django import forms

from .models import CurrencyConverter


class CurrencyConverterForm(forms.Form):
    currency_convert_from = forms.ChoiceField(
        choices=CurrencyConverter.Currency.choices, label="My currency", required=True
    )
    amount = forms.FloatField(label="My amount", required=True, widget=forms.NumberInput(attrs={"min": "0.01"}))
    currency_convert_to = forms.ChoiceField(
        choices=CurrencyConverter.Currency.choices, label="Currency to get", required=True
    )


class ConversionResultForm(forms.Form):
    currency_convert_from = forms.ChoiceField(
        choices=CurrencyConverter.Currency.choices, label="My currency", required=True
    )
    amount = forms.FloatField(label="My amount", required=True)
    currency_convert_to = forms.ChoiceField(
        choices=CurrencyConverter.Currency.choices, label="Currency to get", required=True
    )
    resultamount = forms.FloatField(label="Total", widget=forms.TextInput(attrs={"readonly": "readonly"}))
