# apps/commercial/urls.py
from rest_framework.routers import DefaultRouter
from .views import LeadViewSet, EssaiPlanifieViewSet, CommandeViewSet

router = DefaultRouter()
router.register("leads", LeadViewSet, basename="lead")
router.register("essais", EssaiPlanifieViewSet, basename="essai")
router.register("commandes", CommandeViewSet, basename="commande")

urlpatterns = router.urls