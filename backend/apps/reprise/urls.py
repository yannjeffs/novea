# apps/reprise/urls.py (public)
from rest_framework.routers import DefaultRouter
from .views import DemandeRepriseCreationView

router = DefaultRouter()
router.register("estimation", DemandeRepriseCreationView, basename="estimation-reprise")
urlpatterns = router.urls
