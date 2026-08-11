from rest_framework import viewsets
from .models import Category
from .serializers import CategorySerializer
from users.permissions import IsAdminRole


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class AdminCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminRole]
    lookup_field = 'slug'
    search_fields = ['name', 'slug']
    ordering_fields = ['name', 'sort_order', 'created_at']
