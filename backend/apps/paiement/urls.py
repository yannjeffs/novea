# apps/paiement/urls.py
from django.urls import path
from .views import InitierPaiementView, WebhookMomoView, WebhookOrangeMoneyView

urlpatterns = [
    path("initier/", InitierPaiementView.as_view(), name="initier-paiement"),
    path("webhook/momo/", WebhookMomoView.as_view(), name="webhook-momo"),
    path("webhook/orange-money/", WebhookOrangeMoneyView.as_view(), name="webhook-orange"),
]