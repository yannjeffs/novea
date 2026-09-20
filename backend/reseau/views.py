from rest_framework import viewsets

from .models import Concession
from .serializers import ConcessionSerializer


class ConcessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Concession.objects.filter(actif=True)
    serializer_class = ConcessionSerializer