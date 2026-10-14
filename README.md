# Starlink Data Bundles — Chad Django Demo

A responsive Django storefront for the six data bundles specified for Chad. French is the default language, with English and Arabic (RTL) available. The site displays Chad’s **+235** calling code, and prices are set and validated server-side in FCFA.

## Bundles

| Bundle | Data | Price |
|---|---:|---:|
| Starter Bundle | 120 GB · valid 2 months | 6,500 FCFA |
| Popular Bundle | 250 GB | 11,000 FCFA |
| Elite Bundle | 400 GB | 16,500 FCFA |
| Pro Bundle | 600 GB | 22,000 FCFA |
| Business Bundle | 1 TB | 33,000 FCFA |
| Unlimited Bundle | Unlimited | 55,000 FCFA |

Only the Starter Bundle duration was supplied, so validity for the other offers is not invented.

## Run locally

Python 3.10+ is required. From the project directory:

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000>. On Linux/macOS, `./run.sh` applies migrations and starts the server. The generated SQLite database is excluded from the ZIP.

## Classroom checkout and Telegram alerts

Airtel Money and Moov Money are selectable, but this is a **demo-only checkout**. There is no live payment API, no debit, and no actual transaction. The confirmation page provides a CSRF-protected button to simulate a provider approval; the order remains labelled **unpaid**.

The app does not request or store a customer name, phone number, wallet PIN, OTP, or other personal identifier. It stores only a random demo reference, the selected bundle, price, payment option, and demo status. No OTP/PIN inputs, database columns, session storage, or Telegram payload fields exist for those secrets. In a real integration, the provider must collect and validate its own codes on its official app, USSD or hosted checkout; this Django app does not implement those PIN/OTP screens or validation lengths.

When both Telegram variables are configured, the app automatically sends two **non-personal demo notifications** to the specified bot chat: one when a demo order is created, and one when the mock provider approval is triggered. Messages include only the random reference, bundle/data, FCFA amount, chosen payment option, and an explicit unpaid/demo status. Telegram delivery failure does not block the demo order.

To enable delivery:

1. Create a bot with Telegram’s official [@BotFather](https://t.me/BotFather) and determine the destination `chat_id`.
2. Put the bot token and chat ID into your **local, untracked** `.env` file as `TELEGRAM_BOT_TOKEN=...` and `TELEGRAM_CHAT_ID=...`. The project never includes real values in the ZIP. Do not commit or share the bot token.
3. Restart Django. If either variable is empty, notifications are skipped. This sandbox has no Telegram bot credentials configured, so actual delivery cannot be verified here.

The notifier uses Telegram’s official HTTPS Bot API [`sendMessage`](https://core.telegram.org/bots/api#sendmessage). No matching Telegram integration or credentials are available in this task environment.

## Admin and production notes

The Django admin is at `/admin/`; create an admin user with `python manage.py createsuperuser` if needed. For deployment, configure a strong `DJANGO_SECRET_KEY`, correct `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`, and set `DJANGO_DEBUG=false`. Keep `.env` private. Use HTTPS, rate limits, a production database, and an approved provider integration before any real public payment flow. Django’s built-in runserver is for development only.
