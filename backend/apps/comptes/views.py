# apps/comptes/views.py
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Utilisateur
from .serializers import UtilisateurSerializer, UtilisateurCreationSerializer, MoiSerializer


class EstAdminReseau(permissions.BasePermission):
    """Seul un admin réseau peut créer/modifier des comptes conseillers"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Utilisateur.Role.ADMIN_RESEAU


class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all().order_by("last_name")
    permission_classes = [EstAdminReseau]

    def get_serializer_class(self):
        if self.action == "create":
            return UtilisateurCreationSerializer
        return UtilisateurSerializer


class MoiView(APIView):
    """GET /api/auth/moi/ — appelé par Angular juste après le login pour récupérer le profil"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(MoiSerializer(request.user).data)