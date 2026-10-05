# apps/occasion/search_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_elasticsearch_dsl import Q
from .documents import VehiculeOccasionDocument


class RechercheOccasionView(APIView):
    """GET /api/occasions/recherche/?energie=diesel&prix_max=20000000&certifie=true"""
    permission_classes = [AllowAny]

    def get(self, request):
        params = request.query_params
        search = VehiculeOccasionDocument.search()

        # Filtres à facettes (correspond aux cases à cocher de la maquette)
        if energies := params.getlist("energie"):
            search = search.filter("terms", energie=energies)

        if params.get("prix_max"):
            search = search.filter("range", prix_vente={"lte": params.get("prix_max")})

        if params.get("kilometrage_max"):
            search = search.filter("range", kilometrage={"lte": params.get("kilometrage_max")})

        if params.get("certifie") == "true":
            search = search.filter("term", certifie_novea=True)

        if carrosserie := params.get("carrosserie"):
            search = search.filter("term", carrosserie_nom=carrosserie)

        # Recherche texte libre (nom du modèle, etc.)
        if q := params.get("q"):
            search = search.query(Q("multi_match", query=q, fields=["carrosserie_nom", "concession_nom"]))

        # Pagination
        page = int(params.get("page", 1))
        taille = 12
        search = search[(page - 1) * taille: page * taille]

        try:
            response = search.execute()
            resultats = [hit.to_dict() for hit in response]
            return Response({
                "count": response.hits.total.value,
                "results": resultats,
            })
        except Exception:
            # Fallback PostgreSQL si Elasticsearch est indisponible (voir note de résilience du Lot 1)
            return self._fallback_postgresql(params, page, taille)

    def _fallback_postgresql(self, params, page, taille):
        from .models import VehiculeOccasion
        from .serializers import VehiculeOccasionListeSerializer

        qs = VehiculeOccasion.objects.filter(etape__in=["en_ligne", "reserve"])
        if energies := params.getlist("energie"):
            qs = qs.filter(motorisation__energie__in=energies)
        if params.get("prix_max"):
            qs = qs.filter(prix_vente__lte=params.get("prix_max"))
        if params.get("certifie") == "true":
            qs = qs.filter(certifie_novea=True)

        debut = (page - 1) * taille
        resultats = qs[debut: debut + taille]
        return Response({
            "count": qs.count(),
            "results": VehiculeOccasionListeSerializer(resultats, many=True).data,
            "degrade": True,  # pour que le front puisse signaler le mode dégradé si besoin
        })