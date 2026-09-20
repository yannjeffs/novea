# Modèle de données Novéa Cameroun — notes d'intégration

## Structure

7 apps, dans l'ordre de dépendance (une app ne référence que des apps qui la
précèdent dans cette liste, via des FK en chaîne de caractères pour éviter
les imports circulaires) :

```
core            → utilitaires partagés (pas de modèles concrets, pas de table)
reseau          → Concession
accounts        → Utilisateur (AUTH_USER_MODEL), rôles
catalogue       → VehiculeModele, Motorisation, Finition, Teinte, Habitacle,
                   OptionPack, DocumentVehicule, MediaVehicule
configurateur   → Configuration
commercial      → Lead, Essai
ventes          → VehiculePhysique, Commande, Paiement
```

`core` ne contient que des classes abstraites/utilitaires (`TimestampedModel`,
`generate_reference`) : il n'a pas besoin de `apps.py` ni d'entrée dans
`INSTALLED_APPS`, un simple package Python importable suffit.

## À ajouter dans `settings.py`

```python
INSTALLED_APPS = [
    # ... apps Django/DRF ...
    "django.contrib.postgres",  # requis pour ArrayField (catalogue.OptionPack)
    "accounts",
    "reseau",
    "catalogue",
    "configurateur",
    "commercial",
    "ventes",
]

AUTH_USER_MODEL = "accounts.Utilisateur"
```

⚠️ `AUTH_USER_MODEL` doit être défini **avant la toute première migration** du
projet — s'il existe déjà des migrations avec le `User` par défaut, il faudra
repartir d'une base propre ou passer par une migration de données dédiée.

## Points laissés ouverts (à trancher avec vous)

- **Simulateur de crédit** : `Configuration.mensualite_estimee` existe déjà
  comme champ, mais son calcul n'est pas implémenté — en attente de votre
  décision sur son emplacement (dans le configurateur ou ailleurs).
- **Garanties** : le cahier des charges mentionne des "labels de garantie" et
  "extensions de garantie" en objectif secondaire ; pas encore modélisé en
  tant qu'entité dédiée (`Garantie`), à ajouter quand ce point sera priorisé.
- **Rôles "Transitaire" et "Banque/EMF"** : traités comme des intégrations
  externes (webhooks/API) plutôt que comme des comptes `Utilisateur`, en
  cohérence avec le tableau "Acteurs et rôles" du cahier des charges.

## Prochaines étapes suggérées

1. `python manage.py startapp` n'est pas nécessaire : copiez chaque dossier
   d'app tel quel à la racine du projet Django existant.
2. `python manage.py makemigrations && python manage.py migrate`
3. `admin.py` par app pour l'interface d'administration (non fourni ici,
   dites-moi si vous voulez que je l'ajoute).
4. Sérialiseurs et vues DRF pour exposer l'API REST consommée par Angular.
