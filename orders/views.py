from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from .catalog import get_bundle, get_bundles
from .forms import CheckoutForm
from .models import Order
from .notifications import send_order_notification
from .translations import LANGUAGES, TEXT


def language_for(request):
    language = request.session.get("site_language", "fr")
    return language if language in LANGUAGES else "fr"


def page_context(request, **extra):
    language = language_for(request)
    language_options = (("fr", "FR"), ("en", "EN"), ("ar", "AR"))
    return {"language": language, "direction": "rtl" if language == "ar" else "ltr", "t": TEXT[language], "language_options": language_options, **extra}


@require_GET
def set_language(request, code):
    if code in LANGUAGES:
        request.session["site_language"] = code
    next_url = request.GET.get("next", "/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        next_url = "/"
    return redirect(next_url)


@require_GET
def index(request):
    language = language_for(request)
    return render(request, "orders/index.html", page_context(request, bundles=get_bundles(language)))


@require_http_methods(["GET", "POST"])
def checkout(request, code):
    language = language_for(request)
    bundle = get_bundle(code, language)
    if not bundle:
        raise Http404(TEXT[language]["not_found"])

    labels = {
        "payment_method": TEXT[language]["payment_method"],
        "airtel_name": "Airtel Money",
        "moov_name": "Moov Money",
    }
    form = CheckoutForm(request.POST or None, labels=labels)
    error_message = ""
    selected_payment = request.POST.get("payment_method", "airtel_money") if request.method == "POST" else "airtel_money"

    if request.method == "POST":
        if form.is_valid():
            method = form.cleaned_data["payment_method"]
            order = Order.objects.create(
                bundle_code=bundle["code"],
                bundle_name=bundle["localized_name"],
                data_volume=bundle["volume"] or "Unlimited",
                amount_fcfa=bundle["amount_fcfa"],
                payment_method=method,
            )
            send_order_notification(order, "created")
            return redirect("order_success", reference=order.reference)
        if "payment_method" in form.errors:
            error_message = TEXT[language]["payment_error"]
        else:
            error_message = TEXT[language]["required_error"]

    payment_options = [
        {"code": "airtel_money", "name": "Airtel Money", "copy": TEXT[language]["airtel_copy"], "initial": "A"},
        {"code": "moov_money", "name": "Moov Money", "copy": TEXT[language]["moov_copy"], "initial": "M"},
    ]
    return render(request, "orders/checkout.html", page_context(
        request,
        bundle=bundle,
        form=form,
        error_message=error_message,
        selected_payment=selected_payment,
        payment_options=payment_options,
    ))


@require_GET
def order_success(request, reference):
    order = get_object_or_404(Order, reference=reference)
    reference_display = str(order.reference).split("-")[0].upper()
    language = language_for(request)
    display_volume = TEXT[language]["unlimited_name"] if order.bundle_code == "unlimited" else order.data_volume
    return render(request, "orders/success.html", page_context(request, order=order, reference_display=reference_display, display_volume=display_volume))


@require_POST
def simulate_payment(request, reference):
    order = get_object_or_404(Order, reference=reference)
    if order.status == "demo_created":
        order.status = "demo_approved"
        order.save(update_fields=["status"])
        send_order_notification(order, "simulated_approval")
    return redirect("order_success", reference=order.reference)
