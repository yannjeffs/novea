from rest_framework.routers import DefaultRouter

from .views import OptionPackViewSet, VehiculeModeleViewSet

router = DefaultRouter()
router.register("vehicules", VehiculeModeleViewSet, basename="vehicule")
router.register("options", OptionPackViewSet, basename="option")

urlpatterns = router.urls