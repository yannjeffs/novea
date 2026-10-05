# apps/comptes/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import UtilisateurViewSet, MoiView

router = DefaultRouter()
router.register("utilisateurs", UtilisateurViewSet, basename="utilisateur")

urlpatterns = [path("moi/", MoiView.as_view(), name="moi")] + router.urls
