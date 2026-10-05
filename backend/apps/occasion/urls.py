# apps/occasion/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import VehiculeOccasionDetailViewSet, VehiculeOccasionAdminViewSet
from .search_views import RechercheOccasionView

router_public = DefaultRouter()
router_public.register("", VehiculeOccasionDetailViewSet, basename="occasion-public")

router_admin = DefaultRouter()
router_admin.register("", VehiculeOccasionAdminViewSet, basename="occasion-admin")

urlpatterns_public = [
    path("recherche/", RechercheOccasionView.as_view(), name="recherche-occasion"),
] + router_public.urls

urlpatterns_admin = router_admin.urls