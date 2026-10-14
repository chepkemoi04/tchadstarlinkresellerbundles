import json
from unittest.mock import MagicMock, Mock, patch

from django.test import TestCase, override_settings
from django.urls import reverse

from .catalog import BUNDLES
from .models import Order
from .notifications import send_order_notification


class BundleCatalogTests(TestCase):
    def test_catalog_has_exact_requested_prices_and_amounts(self):
        self.assertEqual([(b["code"], b["volume"], b["amount_fcfa"]) for b in BUNDLES], [
            ("starter", "120 GB", 6500),
            ("popular", "250 GB", 11000),
            ("elite", "400 GB", 16500),
            ("pro", "600 GB", 22000),
            ("business", "1 TB", 33000),
            ("unlimited", None, 55000),
        ])
        self.assertEqual(BUNDLES[0]["validity"]["fr"], "Valable 2 mois")
        self.assertTrue(BUNDLES[1]["featured"])

    def test_home_defaults_to_french_and_shows_both_payment_options(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<html lang="fr" dir="ltr">', html=False)
        self.assertContains(response, "Airtel Money")
        self.assertContains(response, "Moov Money")
        self.assertContains(response, "Starter Bundle")
        self.assertContains(response, "6 500" if "6 500" in response.content.decode() else "6500")

    def test_language_switch_persists_english_and_arabic_rtl(self):
        response = self.client.get(reverse("set_language", args=["en"]), {"next": "/"})
        self.assertEqual(response.status_code, 302)
        self.assertContains(self.client.get(reverse("index")), "Choose your bundle.")
        self.client.get(reverse("set_language", args=["ar"]), {"next": "/"})
        self.assertContains(self.client.get(reverse("index")), '<html lang="ar" dir="rtl">', html=False)

    @patch("orders.views.send_order_notification")
    def test_checkout_persists_no_personal_or_wallet_secret_data(self, notifier):
        response = self.client.post(reverse("checkout", args=["starter"]), {
            "payment_method": "airtel_money",
            "amount_fcfa": "1",
            "full_name": "Must Not Be Stored",
            "phone_number": "12345678",
            "otp_code": "1234",
            "pin_code": "1234",
        })
        order = Order.objects.get()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.amount_fcfa, 6500)
        self.assertEqual(order.payment_method, "airtel_money")
        self.assertEqual(order.status, "demo_created")
        field_names = {field.name for field in Order._meta.get_fields()}
        for forbidden_field in ("full_name", "phone_number", "otp_code", "pin_code", "wallet_pin", "wallet_otp"):
            self.assertNotIn(forbidden_field, field_names)
        confirmation = self.client.get(response.url)
        self.assertContains(confirmation, "Aucun paiement n’a été effectué.")
        self.assertContains(confirmation, "N’entrez jamais votre PIN")
        self.assertNotContains(confirmation, 'name="otp_code"')
        self.assertNotContains(confirmation, 'name="pin_code"')
        notifier.assert_called_once_with(order, "created")

    @patch("orders.views.send_order_notification")
    def test_demo_provider_confirmation_updates_only_unpaid_demo_status(self, notifier):
        self.client.post(reverse("checkout", args=["starter"]), {"payment_method": "moov_money"})
        order = Order.objects.get()
        response = self.client.post(reverse("simulate_payment", args=[order.reference]))
        order.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.status, "demo_approved")
        self.assertContains(self.client.get(response.url), "Aucun paiement réel n’a été effectué.")
        self.assertEqual([call.args[1] for call in notifier.call_args_list], ["created", "simulated_approval"])

    @patch("orders.views.send_order_notification")
    def test_moov_selection_uses_server_price(self, notifier):
        response = self.client.post(reverse("checkout", args=["popular"]), {"payment_method": "moov_money"})
        self.assertEqual(response.status_code, 302)
        order = Order.objects.get()
        self.assertEqual(order.amount_fcfa, 11000)
        self.assertEqual(order.payment_method, "moov_money")

    @patch("orders.views.send_order_notification")
    def test_invalid_payment_does_not_create_an_order(self, notifier):
        response = self.client.post(reverse("checkout", args=["starter"]), {"payment_method": "unknown"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 0)
        notifier.assert_not_called()

    def test_unknown_bundle_returns_404(self):
        self.assertEqual(self.client.get(reverse("checkout", args=["no-such-bundle"])).status_code, 404)


class TelegramNotificationTests(TestCase):
    @override_settings(TELEGRAM_BOT_TOKEN="unit-test-token", TELEGRAM_CHAT_ID="123456")
    @patch("orders.notifications.urlopen")
    def test_notification_payload_contains_only_non_personal_demo_metadata(self, mock_urlopen):
        response = Mock()
        response.read.return_value = b'{"ok":true,"result":{"message_id":1}}'
        context = MagicMock()
        context.__enter__.return_value = response
        context.__exit__.return_value = False
        mock_urlopen.return_value = context
        order = Order.objects.create(
            bundle_code="starter",
            bundle_name="Starter Bundle",
            data_volume="120 GB",
            amount_fcfa=6500,
            payment_method="airtel_money",
        )
        self.assertTrue(send_order_notification(order, "created"))
        request = mock_urlopen.call_args.args[0]
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(payload["chat_id"], "123456")
        self.assertIn("DEMO ORDER CREATED — UNPAID", payload["text"])
        self.assertIn("Starter Bundle", payload["text"])
        for forbidden in ("PIN", "OTP", "12345678", "Must Not Be Stored", "unit-test-token"):
            self.assertNotIn(forbidden, payload["text"])

    @override_settings(TELEGRAM_BOT_TOKEN="", TELEGRAM_CHAT_ID="")
    @patch("orders.notifications.urlopen")
    def test_without_credentials_notification_is_skipped(self, mock_urlopen):
        order = Order.objects.create(
            bundle_code="elite",
            bundle_name="Elite Bundle",
            data_volume="400 GB",
            amount_fcfa=16500,
            payment_method="moov_money",
        )
        self.assertFalse(send_order_notification(order, "created"))
        mock_urlopen.assert_not_called()
