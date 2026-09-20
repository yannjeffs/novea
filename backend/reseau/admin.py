from django.contrib import admin

from .models import Concession


@admin.register(Concession)
class ConcessionAdmin(admin.ModelAdmin):
    list_display = ("nom", "ville", "telephone", "capacite_essai_quotidienne", "actif")
    list_filter = ("ville", "actif")
    search_fields = ("nom", "ville", "adresse")
