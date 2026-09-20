from rest_framework import permissions


class EstPersonnelInterne(permissions.BasePermission):
    """Autorise uniquement le personnel interne (conseiller, chef des ventes, etc.)."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.est_personnel_interne
        )


class EstProprietaireOuPersonnelInterne(permissions.BasePermission):
    """Le client ne voit que ses propres objets ; le personnel interne voit tout."""

    def has_object_permission(self, request, view, obj):
        if request.user.est_personnel_interne:
            return True
        client = getattr(obj, "client", None)
        return client == request.user