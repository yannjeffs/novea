# reprise/models.py
from django.db import models

class DemandeReprise(models.Model):
    """Une demande de reprise, du formulaire en ligne jusqu'à l'offre ferme"""

    class Etape(models.TextChoices):
        ESTIMATION_EN_LIGNE = "estimation_en_ligne", "Estimation en ligne"
        EXPERTISE_PLANIFIEE = "expertise_planifiee", "Expertise planifiée"
        OFFRE_TRANSMISE = "offre_transmise", "Offre transmise"
        OFFRE_ACCEPTEE = "offre_acceptee", "Offre acceptée"
        REFUSEE = "refusee", "Refusée"

    class EtatDeclare(models.TextChoices):
        EXCELLENT = "excellent", "Excellent"
        TRES_BON = "tres_bon", "Très bon"
        BON = "bon", "Bon"

    reference = models.CharField(max_length=20, unique=True)   # "RP-2041"

    # --- Client et véhicule repris (déclaratif, saisi par le client) ---
    nom_client = models.CharField(max_length=150)
    telephone = models.CharField(max_length=20)
    marque_modele = models.CharField(max_length=150)   # "SUV — autre marque" si non-Novéa
    energie = models.CharField(max_length=25)
    annee = models.PositiveIntegerField()
    kilometrage = models.PositiveIntegerField()
    etat_declare = models.CharField(max_length=20, choices=EtatDeclare.choices)
    carnet_entretien_complet = models.BooleanField(default=False)

    concession = models.ForeignKey("reseau.Concession", on_delete=models.SET_NULL, null=True)

    # --- Projet lié (si la reprise finance un achat neuf) ---
    configuration_liee = models.ForeignKey(
        "configurateur.ConfigurationVehicule", on_delete=models.SET_NULL, null=True, blank=True
    )

    # --- Chiffrage à chaque étape ---
    estimation_en_ligne = models.DecimalField(max_digits=12, decimal_places=0)
    valeur_expertise = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    offre_transmise = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    offre_validite_jours = models.PositiveSmallIntegerField(default=7)
    offre_validite_km = models.PositiveIntegerField(default=500)

    etape = models.CharField(max_length=25, choices=Etape.choices, default=Etape.ESTIMATION_EN_LIGNE)
    expert_assigne = models.ForeignKey(
        "comptes.Utilisateur", on_delete=models.SET_NULL, null=True, blank=True, related_name="expertises"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def ecart_estimation_expertise_pct(self):
        """Écart affiché sur le tableau back-office ('-9 %')"""
        if self.valeur_expertise and self.estimation_en_ligne:
            return round((self.valeur_expertise - self.estimation_en_ligne) / self.estimation_en_ligne * 100, 1)
        return None


class RendezVousExpertise(models.Model):
    """Le créneau d'expertise en concession"""
    demande = models.OneToOneField(DemandeReprise, on_delete=models.CASCADE, related_name="rendez_vous")
    concession = models.ForeignKey("reseau.Concession", on_delete=models.PROTECT)
    date_heure = models.DateTimeField()
    realise = models.BooleanField(default=False)


class GrilleDecote(models.Model):
    """Grille de décote interne (pas d'équivalent Argus/SIV au Cameroun) — barème par tranche d'âge/km"""
    marque = models.CharField(max_length=100, blank=True)   # vide = grille par défaut toutes marques
    age_min_mois = models.PositiveIntegerField()
    age_max_mois = models.PositiveIntegerField(null=True, blank=True)
    km_min = models.PositiveIntegerField()
    km_max = models.PositiveIntegerField(null=True, blank=True)
    coefficient_decote = models.DecimalField(max_digits=4, decimal_places=3)   # ex: 0.850 = -15%