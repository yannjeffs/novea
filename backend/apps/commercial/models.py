# commercial/models.py
from django.db import models

class Lead(models.Model):
    """Toute demande entrante : configurateur, site, téléphone, WhatsApp, concession"""

    class Source(models.TextChoices):
        CONFIGURATEUR = "configurateur", "Configurateur"
        SITE = "formulaire_site", "Formulaire site"
        TELEPHONE = "telephone", "Téléphone"
        WHATSAPP = "whatsapp", "WhatsApp"
        CONCESSION = "concession", "Concession"

    class Statut(models.TextChoices):
        NOUVEAU = "nouveau", "Nouveau"
        A_RAPPELER = "a_rappeler", "À rappeler"
        ESSAI_PLANIFIE = "essai_planifie", "Essai planifié"
        DEVIS_ENVOYE = "devis_envoye", "Devis envoyé"
        GAGNE = "gagne", "Gagné"
        PERDU = "perdu", "Perdu"

    reference = models.CharField(max_length=20, unique=True)   # "LD-2418"
    nom_client = models.CharField(max_length=150)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    source = models.CharField(max_length=20, choices=Source.choices)
    concession = models.ForeignKey("reseau.Concession", on_delete=models.SET_NULL, null=True)
    conseiller = models.ForeignKey("comptes.Utilisateur", on_delete=models.SET_NULL, null=True, blank=True)
    configuration = models.ForeignKey(
        "configurateur.ConfigurationVehicule", on_delete=models.SET_NULL, null=True, blank=True
    )
    montant_estime = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.NOUVEAU)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EssaiPlanifie(models.Model):
    """Un créneau d'essai routier, 45 min, par concession"""

    class Statut(models.TextChoices):
        A_CONFIRMER = "a_confirmer", "À confirmer"
        CONFIRME = "confirme", "Confirmé"
        REALISE = "realise", "Réalisé"
        ANNULE = "annule", "Annulé"

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="essais")
    concession = models.ForeignKey("reseau.Concession", on_delete=models.PROTECT)
    conseiller = models.ForeignKey("comptes.Utilisateur", on_delete=models.SET_NULL, null=True)
    vehicule_essai = models.ForeignKey(
        "occasion.VehiculeOccasion", on_delete=models.SET_NULL, null=True, blank=True,
        help_text="Si un véhicule de démo est utilisé"
    )
    date_heure = models.DateTimeField()
    duree_minutes = models.PositiveIntegerField(default=45)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.A_CONFIRMER)
    created_at = models.DateTimeField(auto_now_add=True)


class Commande(models.Model):
    """Suivi de production/livraison, de la signature à la remise des clés"""

    class Etape(models.TextChoices):
        CONFIRMEE = "confirmee", "Commande confirmée"
        PRODUCTION = "production", "En production"
        TRANSPORT = "transport", "Transport maritime"
        DEDOUANEMENT = "dedouanement", "Dédouanement"
        PRETE = "prete", "Prête en concession"
        LIVREE = "livree", "Livrée"

    class TypeFinancement(models.TextChoices):
        COMPTANT = "comptant", "Comptant"
        CREDIT_BANCAIRE = "credit_bancaire", "Crédit bancaire"
        CREDIT_EMF = "credit_emf", "Crédit EMF"
        LLD = "lld", "Location longue durée"

    reference = models.CharField(max_length=20, unique=True)   # "CM-10482"
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, related_name="commandes")
    devis = models.ForeignKey("catalogue.Devis", on_delete=models.SET_NULL, null=True, blank=True)
    reprise = models.OneToOneField(
        "reprise.DemandeReprise", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="commande_liee"
    )
    concession = models.ForeignKey("reseau.Concession", on_delete=models.PROTECT)
    conseiller = models.ForeignKey("comptes.Utilisateur", on_delete=models.SET_NULL, null=True)

    montant_total = models.DecimalField(max_digits=12, decimal_places=0)
    type_financement = models.CharField(max_length=20, choices=TypeFinancement.choices)
    acompte = models.DecimalField(max_digits=12, decimal_places=0, default=0)

    etape = models.CharField(max_length=20, choices=Etape.choices, default=Etape.CONFIRMEE)
    date_livraison_prevue = models.DateField(null=True, blank=True)
    date_livraison_reelle = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EtapeHistorique(models.Model):
    """Trace chaque changement d'étape d'une commande (utile pour le détail 'Étape X sur 6')"""
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name="historique_etapes")
    etape = models.CharField(max_length=20, choices=Commande.Etape.choices)
    date_passage = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(blank=True)