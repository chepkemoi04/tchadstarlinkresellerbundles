from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("language/<str:code>/", views.set_language, name="set_language"),
    path("checkout/<slug:code>/", views.checkout, name="checkout"),
    path("order/<uuid:reference>/", views.order_success, name="order_success"),
    path("order/<uuid:reference>/simulate/", views.simulate_payment, name="simulate_payment"),
]
