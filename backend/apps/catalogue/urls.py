# apps/catalogue/urls.py
from rest_framework.routers import DefaultRouter
from .views import (
    CarrosseriePublicViewSet, CarrosserieAdminViewSet,
    MotorisationAdminViewSet, FinitionAdminViewSet, DevisViewSet,
)

router_public = DefaultRouter()
router_public.register("carrosseries", CarrosseriePublicViewSet, basename="carrosserie-public")

urlpatterns = router_public.urls   # à inclure sous /api/catalogue/
# et router_admin.urls à inclure séparément sous /api/admin/catalogue/