# apps/reseau/views.py
from rest_framework import viewsets, permissions
from .models import Concession
from .serializers import ConcessionSerializer


class ConcessionViewSet(viewsets.ModelViewSet):
    queryset = Concession.objects.filter(active=True)
    serializer_class = ConcessionSerializer
    permission_classes = [permissions.IsAuthenticated]