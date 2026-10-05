# apps/paiement/services/orange_money.py
import requests
from django.conf import settings

def initier_paiement_orange_money(numero_telephone, montant, reference_interne):
    """Déclenche une demande de paiement Orange Money (Web Payment API)"""
    response = requests.post(
        f"{settings.ORANGE_MONEY_API_BASE_URL}/omcoreapis/1.0.2/mp/pay",
        headers={"Authorization": f"Bearer {_obtenir_token_orange()}"},
        json={
            "merchant_key": settings.ORANGE_MONEY_MERCHANT_KEY,
            "currency": "XAF",
            "order_id": reference_interne,
            "amount": str(montant),
            "subscriber_msisdn": numero_telephone,
        },
    )
    response.raise_for_status()
    return response.json()


def _obtenir_token_orange():
    raise NotImplementedError("À configurer avec les identifiants Orange Money Developer")