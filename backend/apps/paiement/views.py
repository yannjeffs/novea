# apps/paiement/views.py
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Paiement
from .serializers import PaiementInitiationSerializer, PaiementSerializer
from .services.momo import initier_paiement_momo
from .services.orange_money import initier_paiement_orange_money


class InitierPaiementView(APIView):
    """POST /api/paiement/initier/ — appelé depuis l'étape 'Essai & réservation'"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PaiementInitiationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        reference = f"PAY-{uuid.uuid4().hex[:10].upper()}"
        paiement = Paiement.objects.create(
            lead_id=data.get("lead"),
            commande_id=data.get("commande"),
            methode=data["methode"],
            numero_telephone=data["numero_telephone"],
            montant=data["montant"],
            reference_interne=reference,
        )

        try:
            if data["methode"] == Paiement.Methode.MTN_MOMO:
                succes = initier_paiement_momo(data["numero_telephone"], data["montant"], reference)
            else:
                succes = initier_paiement_orange_money(data["numero_telephone"], data["montant"], reference)
        except Exception:
            paiement.statut = Paiement.Statut.ECHOUE
            paiement.save()
            return Response({"erreur": "Échec de l'initiation du paiement"}, status=status.HTTP_502_BAD_GATEWAY)

        return Response(PaiementSerializer(paiement).data, status=status.HTTP_202_ACCEPTED)


class WebhookMomoView(APIView):
    """POST appelé par MTN lui-même pour confirmer le résultat — pas d'authentification JWT classique,
    sécurisé autrement (IP whitelist ou signature, à configurer selon la doc MTN)"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        reference = request.data.get("externalId")
        try:
            paiement = Paiement.objects.get(reference_interne=reference)
        except Paiement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        paiement.payload_webhook = request.data
        paiement.statut = Paiement.Statut.REUSSI if request.data.get("status") == "SUCCESSFUL" else Paiement.Statut.ECHOUE
        from django.utils import timezone
        paiement.date_confirmation = timezone.now()
        paiement.save()

        return Response(status=status.HTTP_200_OK)


class WebhookOrangeMoneyView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # Structure à adapter précisément selon la doc Orange Money — squelette identique au principe MTN
        reference = request.data.get("order_id")
        try:
            paiement = Paiement.objects.get(reference_interne=reference)
        except Paiement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        paiement.payload_webhook = request.data
        paiement.statut = Paiement.Statut.REUSSI if request.data.get("status") == "SUCCESS" else Paiement.Statut.ECHOUE
        from django.utils import timezone
        paiement.date_confirmation = timezone.now()
        paiement.save()

        return Response(status=status.HTTP_200_OK)