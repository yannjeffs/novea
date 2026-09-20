from django.contrib import admin

from .models import (
    DocumentVehicule,
    Finition,
    Habitacle,
    MediaVehicule,
    Motorisation,
    OptionPack,
    Teinte,
    VehiculeModele,
)


class MotorisationInline(admin.TabularInline):
    model = Motorisation
    extra = 1


class FinitionInline(admin.TabularInline):
    model = Finition
    extra = 1


class TeinteInline(admin.TabularInline):
    model = Teinte
    extra = 1


class HabitacleInline(admin.TabularInline):
    model = Habitacle
    extra = 1


class MediaVehiculeInline(admin.TabularInline):
    model = MediaVehicule
    extra = 1


class DocumentVehiculeInline(admin.TabularInline):
    model = DocumentVehicule
    extra = 1


@admin.register(VehiculeModele)
class VehiculeModeleAdmin(admin.ModelAdmin):
    list_display = ("nom", "carrosserie", "energie", "prix_base", "disponible", "ordre_affichage")
    list_filter = ("carrosserie", "energie", "disponible")
    search_fields = ("nom",)
    prepopulated_fields = {"slug": ("nom",)}
    inlines = [
        MotorisationInline,
        FinitionInline,
        TeinteInline,
        HabitacleInline,
        MediaVehiculeInline,
        DocumentVehiculeInline,
    ]


@admin.register(OptionPack)
class OptionPackAdmin(admin.ModelAdmin):
    list_display = ("nom", "categorie", "prix", "disponible")
    list_filter = ("categorie", "disponible")
    search_fields = ("nom",)
    filter_horizontal = ("modeles_compatibles",)
