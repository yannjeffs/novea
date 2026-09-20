from django.contrib import admin

from .models import Commande, Paiement, VehiculePhysique


class PaiementInline(admin.TabularInline):
    model = Paiement
    extra = 0
    readonly_fields = ("reference", "created_at")


@admin.register(VehiculePhysique)
class VehiculePhysiqueAdmin(admin.ModelAdmin):
    list_display = ("vin", "modele", "finition", "statut", "concession", "date_arrivee")
    list_filter = ("statut", "concession", "modele")
    search_fields = ("vin",)


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "client",
        "concession",
        "montant_total",
        "acompte_montant",
        "etape",
        "financement_type",
        "date_prevue_livraison",
    )
    list_filter = ("etape", "financement_type", "concession")
    search_fields = ("reference", "client__username", "client__last_name")
    readonly_fields = ("reference", "created_at", "updated_at")
    inlines = [PaiementInline]


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ("reference", "commande", "canal", "montant", "statut", "created_at")
    list_filter = ("canal", "statut")
    search_fields = ("reference", "reference_externe", "commande__reference")
    readonly_fields = ("reference", "created_at", "updated_at")
