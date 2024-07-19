from django.urls import reverse_lazy
from django.views.generic import FormView
from rest_framework import viewsets
from django.shortcuts import render

from .forms import CurrencyConverterForm, ConversionResultForm
from .models import CurrencyConverter
from .serializers import CurrencyConverterSerializer


class CurrencyConverterView(FormView):
    template_name = "converter/index.html"
    form_class = CurrencyConverterForm
    success_url = reverse_lazy("converter:home")

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        print(self.request.POST)
        form = self.form_class(request.POST)
        currency_convert_from = self.request.POST.get("currency_convert_from")
        amount = self.request.POST.get("amount")
        currency_convert_to = self.request.POST.get("currency_convert_to")

        cur_from = CurrencyConverter.objects.filter(currency=currency_convert_from).order_by("-updated_date").first()
        cur_to = CurrencyConverter.objects.filter(currency=currency_convert_to).order_by("-updated_date").first()

        if cur_from and cur_to:
            amount = float(amount)
            result_amount = amount * cur_to.cur_to_usd / cur_from.cur_to_usd
            result_amount = round(result_amount, 2)
            result_form = ConversionResultForm(
                initial={
                    "currency_convert_from": currency_convert_from,
                    "amount": amount,
                    "currency_convert_to": currency_convert_to,
                    "resultamount": result_amount,
                }
            )
            return render(request, self.template_name, {"form": form, "result_form": result_form})

        else:
            error = "Rate not found."
            return render(request, self.template_name, {"form": form, "error": error})

        return render(request, self.template_name, {"form": form})


class CurrencyConverterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CurrencyConverter.objects.all()
    serializer_class = CurrencyConverterSerializer
