from rest_framework.routers import DefaultRouter

from .views import ConfigurationViewSet

router = DefaultRouter()
router.register("configurations", ConfigurationViewSet, basename="configuration")

urlpatterns = router.urls