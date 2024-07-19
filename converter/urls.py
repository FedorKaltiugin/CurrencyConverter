from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "converter"
router = DefaultRouter()
router.register(r"currencyconverter", views.CurrencyConverterViewSet)

urlpatterns = [
    path("", views.CurrencyConverterView.as_view(), name="home"),
    path("currencies/", views.CurrencyConverterViewSet.as_view({"get": "list"}), name="currency-list"),
    path("currencies/<int:pk>/", views.CurrencyConverterViewSet.as_view({"get": "retrieve"}), name="currency-detail"),
    path("api/", include(router.urls)),
]
