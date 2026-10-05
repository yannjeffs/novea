# apps/configurateur/urls.py
from rest_framework.routers import DefaultRouter
from .views import ConfigurationVehiculeViewSet

router = DefaultRouter()
router.register("configurations", ConfigurationVehiculeViewSet, basename="configuration")

urlpatterns = router.urls