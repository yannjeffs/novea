from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Utilisateur


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ("username", "get_full_name", "role", "telephone", "concession", "is_active")
    list_filter = ("role", "concession", "is_active", "is_staff")
    search_fields = ("username", "first_name", "last_name", "email", "telephone")
    ordering = ("username",)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Novéa Cameroun",
            {
                "fields": (
                    "role",
                    "telephone",
                    "langue_preferee",
                    "concession",
                    "raison_sociale",
                    "numero_contribuable",
                    "deux_facteurs_active",
                )
            },
        ),
    )

    @admin.display(description="Nom complet")
    def get_full_name(self, obj):
        return obj.get_full_name() or "—"
