from rest_framework import serializers

from .models import Concession


class ConcessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concession
        fields = "__all__"