from rest_framework import generics, permissions
from .models import Company, PartnershipRequest
from .serializers import CompanySerializer, PartnershipRequestSerializer
from users.permissions import IsAdminRole


class CompanyView(generics.RetrieveAPIView):
    serializer_class = CompanySerializer

    def get_object(self):
        return Company.load()


class PartnershipRequestCreateView(generics.CreateAPIView):
    serializer_class = PartnershipRequestSerializer


class AdminPartnershipRequestListView(generics.ListAPIView):
    serializer_class = PartnershipRequestSerializer
    permission_classes = [IsAdminRole]
    search_fields = ['full_name', 'company_name']
    ordering_fields = ['created_at', 'status']

    def get_queryset(self):
        return PartnershipRequest.objects.all()
