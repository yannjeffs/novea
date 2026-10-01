# occasion/documents.py
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import VehiculeOccasion

@registry.register_document
class VehiculeOccasionDocument(Document):
    energie = fields.KeywordField(attr="motorisation.energie")
    carrosserie_nom = fields.KeywordField(attr="carrosserie.nom")
    concession_nom = fields.KeywordField(attr="concession.nom")
    prix_vente = fields.FloatField()
    kilometrage = fields.IntegerField()
    annee_mise_circulation = fields.IntegerField()
    certifie_novea = fields.BooleanField()
    etape = fields.KeywordField()

    class Index:
        name = "vehicules_occasion"

    class Django:
        model = VehiculeOccasion
        # on n'indexe que les véhicules effectivement visibles à la recherche publique
        related_models = []

    def get_queryset(self):
        return super().get_queryset().filter(etape__in=[
            VehiculeOccasion.Etat.EN_LIGNE, VehiculeOccasion.Etat.RESERVE
        ])