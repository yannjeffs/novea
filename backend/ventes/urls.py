from rest_framework.routers import DefaultRouter

from .views import CommandeViewSet, PaiementViewSet, VehiculePhysiqueViewSet

router = DefaultRouter()
router.register("vehicules-physiques", VehiculePhysiqueViewSet, basename="vehicule-physique")
router.register("commandes", CommandeViewSet, basename="commande")
router.register("paiements", PaiementViewSet, basename="paiement")

urlpatterns = router.urls