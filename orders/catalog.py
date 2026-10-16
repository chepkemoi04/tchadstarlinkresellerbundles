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


def get_bundles(lang="fr"):
    """Returns the full list of bundles with localized names and validity."""
    localized_list = []
    for bundle in BUNDLES:
        b_copy = bundle.copy()
        b_copy["localized_name"] = b_copy["name"].get(lang, b_copy["name"].get("fr", ""))
        val = b_copy.get("validity")
        if isinstance(val, dict):
            b_copy["localized_validity"] = val.get(lang, val.get("fr", ""))
        else:
            b_copy["localized_validity"] = None
        localized_list.append(b_copy)
    return localized_list


def get_bundle(code, lang="fr"):
    """Returns a specific bundle matching the given code with localized attributes."""
    for bundle in BUNDLES:
        if bundle["code"] == code:
            b_copy = bundle.copy()
            b_copy["localized_name"] = b_copy["name"].get(lang, b_copy["name"].get("fr", ""))
            val = b_copy.get("validity")
            if isinstance(val, dict):
                b_copy["localized_validity"] = val.get(lang, val.get("fr", ""))
            else:
                b_copy["localized_validity"] = None
            return b_copy
    return None