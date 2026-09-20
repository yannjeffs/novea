from rest_framework.routers import DefaultRouter

from .views import EssaiViewSet, LeadViewSet

router = DefaultRouter()
router.register("leads", LeadViewSet, basename="lead")
router.register("essais", EssaiViewSet, basename="essai")

urlpatterns = router.urls