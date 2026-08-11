from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Brand
from .serializers import (
    ProductListSerializer, ProductDetailSerializer, ProductRelatedSerializer,
    BrandSerializer,
)
from users.permissions import IsAdminRole


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = BrandSerializer
    lookup_field = 'slug'


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related('category', 'brand')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'category__slug': ['exact'],
        'brand__slug': ['exact'],
        'price': ['gte', 'lte'],
        'rating': ['gte'],
        'is_popular': ['exact'],
        'is_featured': ['exact'],
        'badge': ['exact'],
    }
    search_fields = ['name', 'description', 'ingredients', 'sku']
    ordering_fields = ['price', 'rating', 'created_at', 'review_count', 'name']
    ordering = ['-created_at']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    @action(detail=True, methods=['get'], url_path='related')
    def related(self, request, slug=None):
        product = self.get_object()
        related = Product.objects.filter(
            category=product.category, is_active=True
        ).exclude(id=product.id)[:8]
        serializer = ProductRelatedSerializer(related, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='popular')
    def popular(self, request):
        products = Product.objects.filter(is_active=True, is_popular=True)[:12]
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='featured')
    def featured(self, request):
        products = Product.objects.filter(is_active=True, is_featured=True)[:12]
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='new')
    def new_arrivals(self, request):
        products = Product.objects.filter(is_active=True).order_by('-created_at')[:12]
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)
