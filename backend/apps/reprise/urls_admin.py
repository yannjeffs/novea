# apps/reprise/urls_admin.py (back-office)
from rest_framework.routers import DefaultRouter
from .views import DemandeRepriseAdminViewSet

router_admin = DefaultRouter()
router_admin.register("demandes", DemandeRepriseAdminViewSet, basename="reprise-admin")
urlpatterns = router_admin.urls