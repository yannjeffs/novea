from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import OptionPack, VehiculeModele
from .serializers import (
    OptionPackSerializer,
    VehiculeModeleDetailSerializer,
    VehiculeModeleListSerializer,
)


class VehiculeModeleViewSet(viewsets.ReadOnlyModelViewSet):
    """Catalogue public — lecture seule, filtrable par énergie/carrosserie, triable par prix."""

    queryset = VehiculeModele.objects.filter(disponible=True).prefetch_related(
        "motorisations", "finitions", "teintes", "habitacles", "medias", "documents", "options"
    )
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["energie", "carrosserie"]
    search_fields = ["nom", "description"]
    ordering_fields = ["prix_base", "puissance_ch"]

    def get_serializer_class(self):
        if self.action == "list":
            return VehiculeModeleListSerializer
        return VehiculeModeleDetailSerializer


class OptionPackViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OptionPack.objects.filter(disponible=True)
    serializer_class = OptionPackSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["categorie"]