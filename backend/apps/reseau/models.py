# reseau/models.py
from django.db import models

class Concession(models.Model):
    nom = models.CharField(max_length=100)          # "Douala — Bonapriso"
    ville = models.CharField(max_length=50)
    adresse = models.CharField(max_length=255)       # "Boulevard de la Liberté, face Orca"
    telephone = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    capacite_essais_simultanes = models.PositiveSmallIntegerField(default=1)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)