# orders/catalog.py

BUNDLES = [
    {
        "code": "starter",
        "name": {"fr": "Forfait Starter", "en": "Starter Bundle", "ar": "باقة البداية"},
        "volume": "120 GB",
        "amount_fcfa": 6500,
        "validity": {"fr": "Valable 2 mois", "en": "Valid for 2 months", "ar": "صالحة لمدة شهرين"},
        "featured": False,
    },
    {
        "code": "advanced",
        "name": {"fr": "Forfait Advanced", "en": "Advanced Bundle", "ar": "باقة متقدمة"},
        "volume": "250 GB",
        "amount_fcfa": 11000,
        "validity": {"fr": "Valable 2 mois", "en": "Valid for 2 months", "ar": "صالحة لمدة شهرين"},
        "featured": True,
    },
    {
        "code": "elite",
        "name": {"fr": "Forfait Elite", "en": "Elite Bundle", "ar": "باقة النخبة"},
        "volume": "400 GB",
        "amount_fcfa": 16500,
        "validity": {"fr": "Valable 2 mois", "en": "Valid for 2 months", "ar": "صالحة لمدة شهرين"},
        "featured": False,
    },
    {
        "code": "pro",
        "name": {"fr": "Forfait Pro", "en": "Pro Bundle", "ar": "باقة برو"},
        "volume": "600 GB",
        "amount_fcfa": 22000,
        "validity": None,
        "featured": False,
    },
    {
        "code": "business",
        "name": {"fr": "Forfait Business", "en": "Business Bundle", "ar": "باقة الأعمال"},
        "volume": "1 TB",
        "amount_fcfa": 33000,
        "validity": None,
        "featured": False,
    },
    {
        "code": "unlimited",
        "name": {"fr": "Forfait Unlimited", "en": "Unlimited Bundle", "ar": "باقة غير محدودة"},
        "volume": None,
        "amount_fcfa": 55000,
        "validity": None,
        "featured": False,
    },
]


def get_bundles():
    """Returns the full list of bundles."""
    return BUNDLES


def get_bundle(code):
    """Returns a specific bundle matching the given code, or None if not found."""
    for bundle in BUNDLES:
        if bundle["code"] == code:
            return bundle
    return None