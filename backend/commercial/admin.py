from django.contrib import admin

from .models import Essai, Lead


class EssaiInline(admin.TabularInline):
    model = Essai
    extra = 0
    fields = ("date_heure", "concession", "conseiller", "vehicule_demo", "statut")


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "nom_contact",
        "source",
        "statut",
        "energie_interet",
        "conseiller",
        "concession",
        "created_at",
    )
    list_filter = ("statut", "source", "concession", "energie_interet")
    search_fields = ("reference", "nom_contact", "email_contact", "telephone_contact")
    readonly_fields = ("reference", "created_at", "updated_at")
    inlines = [EssaiInline]


@admin.register(Essai)
class EssaiAdmin(admin.ModelAdmin):
    list_display = ("lead", "date_heure", "concession", "conseiller", "statut")
    list_filter = ("statut", "concession")
    date_hierarchy = "date_heure"
