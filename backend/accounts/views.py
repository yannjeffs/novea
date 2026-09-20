from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import UtilisateurSerializer


class ProfilView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/v1/accounts/moi/ — profil de l'utilisateur connecté."""

    serializer_class = UtilisateurSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user