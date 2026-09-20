from rest_framework.routers import DefaultRouter

from .views import ConcessionViewSet

router = DefaultRouter()
router.register("concessions", ConcessionViewSet, basename="concession")

urlpatterns = router.urls