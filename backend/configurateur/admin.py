from django.contrib import admin

from .models import Configuration


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ("reference", "client", "modele", "finition", "prix_total", "statut", "created_at")
    list_filter = ("statut", "modele")
    search_fields = ("reference", "client__username", "client__last_name")
    readonly_fields = ("reference", "prix_total", "created_at", "updated_at")
    filter_horizontal = ("options",)
