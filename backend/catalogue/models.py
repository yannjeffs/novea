"""
Catalogue des véhicules neufs Novéa : modèles, motorisations, finitions,
teintes, habitacles, options/packs, médias et documentation.
"""
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


class TypeEnergie(models.TextChoices):
    ESSENCE = "essence", "Essence"
    DIESEL = "diesel", "Diesel"
    HYBRIDE = "hybride", "Hybride"
    HYBRIDE_RECHARGEABLE = "hybride_rechargeable", "Hybride rechargeable"
    ELECTRIQUE = "electrique", "Électrique"


class TypeCarrosserie(models.TextChoices):
    BERLINE = "berline", "Berline"
    SUV = "suv", "SUV"
    CITADINE = "citadine", "Citadine"
    BREAK = "break", "Break"
    PICKUP = "pickup", "Pick-up"
    MONOSPACE = "monospace", "Monospace"


class BoiteVitesses(models.TextChoices):
    MANUELLE = "manuelle", "Manuelle"
    AUTOMATIQUE = "automatique", "Automatique"


class VehiculeModele(models.Model):
    """Un modèle au catalogue (ex : Novéa S6), indépendant du stock physique (VIN)."""

    nom = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    carrosserie = models.CharField(max_length=20, choices=TypeCarrosserie.choices)
    energie = models.CharField(max_length=25, choices=TypeEnergie.choices)
    prix_base = models.DecimalField(max_digits=12, decimal_places=0, validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)

    # Attributs spécifiques électrique / hybride rechargeable
    autonomie_km = models.PositiveIntegerField(null=True, blank=True)
    capacite_batterie_kwh = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    temps_recharge_minutes = models.PositiveIntegerField(null=True, blank=True)

    # Attributs thermique / hybride
    consommation_l_100km = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)

    puissance_ch = models.PositiveSmallIntegerField(null=True, blank=True)
    disponible = models.BooleanField(default=True)
    ordre_affichage = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Modèle de véhicule"
        verbose_name_plural = "Modèles de véhicules"
        ordering = ["ordre_affichage", "nom"]

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


class Motorisation(models.Model):
    """Détail technique de la ou des motorisations disponibles pour un modèle."""

    modele = models.ForeignKey(VehiculeModele, on_delete=models.CASCADE, related_name="motorisations")
    architecture = models.CharField(
        max_length=100, help_text="Ex : 4 cylindres 2.0 essence + 2 moteurs électriques"
    )
    cylindree_cm3 = models.PositiveIntegerField(null=True, blank=True)
    boite = models.CharField(max_length=20, choices=BoiteVitesses.choices)
    couple_nm = models.PositiveSmallIntegerField(null=True, blank=True)
    tension_batterie_v = models.PositiveSmallIntegerField(null=True, blank=True)
    temps_0_100_s = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    class Meta:
        verbose_name = "Motorisation"
        verbose_name_plural = "Motorisations"

    def __str__(self):
        return f"{self.modele} — {self.architecture}"


class Finition(models.Model):
    modele = models.ForeignKey(VehiculeModele, on_delete=models.CASCADE, related_name="finitions")
    nom = models.CharField(max_length=100)
    supplement_prix = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    puissance_ch = models.PositiveSmallIntegerField(null=True, blank=True)
    autonomie_km = models.PositiveIntegerField(null=True, blank=True)
    equipements_inclus = models.TextField(blank=True, help_text="Liste des équipements, un par ligne.")
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Finition"
        verbose_name_plural = "Finitions"
        ordering = ["modele", "ordre"]
        unique_together = ("modele", "nom")

    def __str__(self):
        return f"{self.modele} {self.nom}"


class Teinte(models.Model):
    modele = models.ForeignKey(VehiculeModele, on_delete=models.CASCADE, related_name="teintes")
    nom = models.CharField(max_length=50)
    code_hex = models.CharField(max_length=7, help_text="Ex : #1C1C1C")
    supplement_prix = models.DecimalField(max_digits=12, decimal_places=0, default=0)

    class Meta:
        verbose_name = "Teinte"
        verbose_name_plural = "Teintes"
        unique_together = ("modele", "nom")

    def __str__(self):
        return f"{self.modele} — {self.nom}"


class Habitacle(models.Model):
    modele = models.ForeignKey(VehiculeModele, on_delete=models.CASCADE, related_name="habitacles")
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    supplement_prix = models.DecimalField(max_digits=12, decimal_places=0, default=0)

    class Meta:
        verbose_name = "Habitacle"
        verbose_name_plural = "Habitacles"
        unique_together = ("modele", "nom")

    def __str__(self):
        return f"{self.modele} — {self.nom}"


class CategorieOption(models.TextChoices):
    CONFORT = "confort", "Confort"
    SECURITE = "securite", "Sécurité"
    MULTIMEDIA = "multimedia", "Multimédia et navigation"
    STYLE = "style", "Style et jantes"


class OptionPack(models.Model):
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=12, decimal_places=0)
    categorie = models.CharField(max_length=20, choices=CategorieOption.choices)
    energies_compatibles = ArrayField(
        base_field=models.CharField(max_length=25, choices=TypeEnergie.choices),
        blank=True,
        default=list,
        help_text="Vide = compatible avec toutes les énergies.",
    )
    modeles_compatibles = models.ManyToManyField(VehiculeModele, related_name="options", blank=True)
    disponible = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Option / Pack"
        verbose_name_plural = "Options / Packs"

    def __str__(self):
        return self.nom


class TypeDocument(models.TextChoices):
    MANUEL_UTILISATEUR = "manuel_utilisateur", "Manuel utilisateur"
    FICHE_TECHNIQUE = "fiche_technique", "Fiche technique"
    GARANTIE = "garantie", "Conditions de garantie"


class DocumentVehicule(models.Model):
    modele = models.ForeignKey(VehiculeModele, on_delete=models.CASCADE, related_name="documents")
    type_document = models.CharField(max_length=25, choices=TypeDocument.choices)
    langue = models.CharField(max_length=2, choices=[("fr", "Français"), ("en", "Anglais")], default="fr")
    fichier = models.FileField(upload_to="documents/%Y/%m/")

    class Meta:
        verbose_name = "Document véhicule"
        verbose_name_plural = "Documents véhicule"

    def __str__(self):
        return f"{self.modele} — {self.get_type_document_display()} ({self.langue})"


class TypeMedia(models.TextChoices):
    PHOTO = "photo", "Photo"
    VIDEO = "video", "Vidéo"


class VueMedia(models.TextChoices):
    EXTERIEUR = "exterieur", "Extérieur"
    INTERIEUR = "interieur", "Intérieur"


class MediaVehicule(models.Model):
    modele = models.ForeignKey(VehiculeModele, on_delete=models.CASCADE, related_name="medias")
    type_media = models.CharField(max_length=10, choices=TypeMedia.choices, default=TypeMedia.PHOTO)
    vue = models.CharField(max_length=10, choices=VueMedia.choices, default=VueMedia.EXTERIEUR)
    fichier = models.FileField(upload_to="medias/%Y/%m/")
    legende = models.CharField(max_length=150, blank=True)
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Média véhicule"
        verbose_name_plural = "Médias véhicule"
        ordering = ["modele", "ordre"]

    def __str__(self):
        return f"{self.modele} — {self.get_type_media_display()} #{self.ordre}"
