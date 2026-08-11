from rest_framework import serializers
from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ('id', 'title', 'description', 'image', 'issued_by', 'issued_date', 'expiry_date', 'is_active', 'order')
