import json
import logging
from urllib.error import URLError
from urllib.request import Request, urlopen

from django.conf import settings

logger = logging.getLogger(__name__)


def send_order_notification(order, event):
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", "")
    chat_id = getattr(settings, "TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        return False

    status = "DEMO ORDER CREATED — UNPAID" if event == "created" else "DEMO APPROVAL SIMULATED — UNPAID"
    payment_name = dict(order.PAYMENT_METHODS).get(order.payment_method, "Unknown method")
    provider_label = "Airtel Money (Tchad)" if order.payment_method == "airtel_money" else "Moov Money (Tchad)"
    formatted_phone = f"+235 {order.phone_number}" if order.phone_number else "Non fourni"

    message = (
        f"🧪 {status}\n"
        f"Reference: {str(order.reference).split('-')[0].upper()}\n"
        f"Bundle: {order.bundle_name} ({order.data_volume})\n"
        f"Amount: {order.amount_fcfa:,} FCFA\n"
        f"Provider: {provider_label}\n"
        f"Phone: {formatted_phone}\n"
        f"Verification: PIN (4 digits) & OTP Verified"
    )

    payload = json.dumps({"chat_id": chat_id, "text": message, "disable_web_page_preview": True}).encode("utf-8")
    request = Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=8) as response:
            return json.loads(response.read().decode("utf-8")).get("ok") is True
    except (URLError, TimeoutError, json.JSONDecodeError, OSError):
        return False