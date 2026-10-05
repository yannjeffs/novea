from rest_framework.routers import DefaultRouter
from .views import (
    CarrosseriePublicViewSet, CarrosserieAdminViewSet,
    MotorisationAdminViewSet, FinitionAdminViewSet, DevisViewSet,
)

router_admin = DefaultRouter()
router_admin.register("carrosseries", CarrosserieAdminViewSet, basename="carrosserie-admin")
router_admin.register("motorisations", MotorisationAdminViewSet, basename="motorisation-admin")
router_admin.register("finitions", FinitionAdminViewSet, basename="finition-admin")
router_admin.register("devis", DevisViewSet, basename="devis-admin")

urlpatterns = router_admin.urls