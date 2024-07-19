from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import CurrencyConverter
from .serializers import CurrencyConverterSerializer


class CurrencyConverterTest(TestCase):
    def setUp(self):
        self.usd = CurrencyConverter.objects.create(currency=CurrencyConverter.Currency.USD, cur_to_usd=1.0)
        self.eur = CurrencyConverter.objects.create(currency=CurrencyConverter.Currency.EUR, cur_to_usd=0.85)

    def test_currency_creation(self):
        # Testing currency creation
        usd = CurrencyConverter.objects.get(currency="USD")
        eur = CurrencyConverter.objects.get(currency="EUR")
        self.assertEqual(usd.cur_to_usd, 1.0)
        self.assertEqual(eur.cur_to_usd, 0.85)

    def test_currency_update(self):
        # Testing currency update
        usd = CurrencyConverter.objects.get(currency="USD")
        usd.cur_to_usd = 1.1
        usd.save()
        updated_usd = CurrencyConverter.objects.get(currency="USD")
        self.assertEqual(updated_usd.cur_to_usd, 1.1)

    def test_currency_deletion(self):
        # Testing currency delete
        usd = CurrencyConverter.objects.get(currency="USD")
        usd.delete()
        with self.assertRaises(CurrencyConverter.DoesNotExist):
            CurrencyConverter.objects.get(currency="USD")

    def test_currency_choice(self):
        # Testing correctness of the currency selection
        usd = CurrencyConverter.objects.get(currency="USD")
        self.assertEqual(usd.get_currency_display(), "US dollar")
        eur = CurrencyConverter.objects.get(currency="EUR")
        self.assertEqual(eur.get_currency_display(), "Euro")

    def test_get_currencies(self):
        # Testing retrieving list of currency rates
        response = self.client.get(reverse("currency-list"))
        currencies = CurrencyConverter.objects.all()
        serializer = CurrencyConverterSerializer(currencies, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_currency(self):
        # Testing retrieving a single currency rate
        response = self.client.get(reverse("currency-detail", kwargs={"pk": self.usd.pk}))
        currency = CurrencyConverter.objects.get(pk=self.usd.pk)
        serializer = CurrencyConverterSerializer(currency)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_currency_list_url(self):
        # Testing the currency list URL resolves correctly
        response = self.client.get("/currencies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_currency_detail_url(self):
        # Test the currency detail URL resolves correctly
        response = self.client.get(f"/currencies/{self.usd.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CurrencyConverterSerializerTest(TestCase):
    def setUp(self):
        # Set up test data and serializer
        self.currency_data = {"currency": "USD", "cur_to_usd": 1.0}
        self.currency = CurrencyConverter.objects.create(**self.currency_data)
        self.serializer = CurrencyConverterSerializer(instance=self.currency)

    def test_contains_expected_fields(self):
        # Ensure the serializer contains the expected fields
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(["currency", "cur_to_usd"]))

    def test_currency_field_content(self):
        # Ensure the currency field content is correct
        data = self.serializer.data
        self.assertEqual(data["currency"], self.currency_data["currency"])

    def test_cur_to_usd_field_content(self):
        # Ensure the cur_to_usd field content is correct
        data = self.serializer.data
        self.assertEqual(data["cur_to_usd"], self.currency_data["cur_to_usd"])

    def test_valid_serialization(self):
        # Ensure valid serialization
        serializer = CurrencyConverterSerializer(data=self.currency_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serialization(self):
        # Ensure invalid serialization when cur_to_usd is missing
        invalid_data = {"currency": "USD"}
        serializer = CurrencyConverterSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(["cur_to_usd"]))


class CurrencyConverterTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        CurrencyConverter.objects.create(currency="USD", cur_to_usd=1.0)
        CurrencyConverter.objects.create(currency="EUR", cur_to_usd=0.85)

    def test_get_currencies(self):
        response = self.client.get(reverse("converter:currency-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)
        self.assertIn("currency", response.data[0])
        self.assertIn("cur_to_usd", response.data[0])

    def test_get_single_currency(self):
        usd = CurrencyConverter.objects.get(currency="USD")
        response = self.client.get(reverse("converter:currency-detail", kwargs={"pk": usd.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["currency"], "USD")
        self.assertEqual(response.data["cur_to_usd"], 1.0)


class CurrencyConverterViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.usd = CurrencyConverter.objects.create(currency="USD", cur_to_usd=1.0)
        self.eur = CurrencyConverter.objects.create(currency="EUR", cur_to_usd=0.85)

    def test_index_get(self):
        response = self.client.get(reverse("converter:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "converter/index.html")

    def test_index_post(self):
        data = {"ihavecurrency": "USD", "ihaveamount": 100, "iwantcurrency": "EUR"}
        response = self.client.post(reverse("converter:home"), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("ihavecurrency", response.context)
        self.assertIn("ihaveamount", response.context)
        self.assertIn("iwantcurrency", response.context)
        self.assertIn("iwantamount", response.context)

    def test_index_post_invalid_form(self):
        data = {
            "ihavecurrency": "USD",
            "iwantcurrency": "EUR",
        }
        response = self.client.post(reverse("converter:home"), data)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertIn("form_errors", response.context)
        self.assertIn("ihaveamount", response.context["form_errors"])
        self.assertEqual(response.context["form_errors"]["ihaveamount"], ["This field is required."])


class CurrencyConverterViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.eur = CurrencyConverter.objects.create(currency="EUR", cur_to_usd=0.85)
        self.usd = CurrencyConverter.objects.create(currency="USD", cur_to_usd=1.0)

    def test_currency_converter_list(self):
        response = self.client.get(reverse("converter:currency-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)

    def test_currency_converter_detail(self):
        response = self.client.get(reverse("converter:currency-detail", args=[self.eur.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["currency"], "EUR")
        self.assertEqual(response.data["cur_to_usd"], 0.85)
