# apps/paiement/services/momo.py
import requests
from django.conf import settings

def initier_paiement_momo(numero_telephone, montant, reference_interne):
    """Déclenche une demande de paiement MTN MoMo (Collection API)"""
    response = requests.post(
        f"{settings.MOMO_API_BASE_URL}/collection/v1_0/requesttopay",
        headers={
            "Authorization": f"Bearer {_obtenir_token_momo()}",
            "X-Reference-Id": reference_interne,
            "X-Target-Environment": settings.MOMO_ENVIRONMENT,
            "Ocp-Apim-Subscription-Key": settings.MOMO_SUBSCRIPTION_KEY,
        },
        json={
            "amount": str(montant),
            "currency": "XAF",
            "externalId": reference_interne,
            "payer": {"partyIdType": "MSISDN", "partyId": numero_telephone},
            "payerMessage": "Acompte Novéa Cameroun",
        },
    )
    response.raise_for_status()
    return response.status_code == 202  # 202 = demande acceptée, en attente de confirmation


def _obtenir_token_momo():
    # Appel à l'endpoint d'authentification MTN MoMo — à compléter avec tes identifiants sandbox/prod
    raise NotImplementedError("À configurer avec les identifiants MTN MoMo Developer")