from rest_framework import serializers
from .models import Product, ProductImage, ProductVariant, Brand


class FlexibleImageField(serializers.ImageField):
    """Returns external URLs as-is, local files with MEDIA_URL prefix."""
    def to_representation(self, value):
        if not value:
            return ''
        url = str(value)
        if url.startswith('http://') or url.startswith('https://'):
            return url
        if hasattr(value, 'url'):
            return value.url
        return url


class BrandSerializer(serializers.ModelSerializer):
    image = FlexibleImageField(read_only=True)

    class Meta:
        model = Brand
        fields = ('id', 'name', 'slug', 'description', 'image', 'is_active')


class ProductImageSerializer(serializers.ModelSerializer):
    image = FlexibleImageField(read_only=True)

    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'alt_text', 'order')


class ProductVariantSerializer(serializers.ModelSerializer):
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = ProductVariant
        fields = ('id', 'name', 'sku', 'price_adjustment', 'final_price', 'stock', 'is_active')


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True, default='')
    discount_percent = serializers.IntegerField(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    image = FlexibleImageField(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'price', 'old_price', 'discount_percent',
            'image', 'badge', 'is_popular', 'is_featured', 'rating', 'review_count',
            'category', 'category_name', 'brand', 'brand_name', 'stock', 'is_in_stock',
            'average_rating', 'sku',
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True, default='')
    discount_percent = serializers.IntegerField(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    image = FlexibleImageField(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'description', 'price', 'old_price',
            'discount_percent', 'image', 'ingredients', 'badge', 'sku', 'stock',
            'is_active', 'is_popular', 'is_featured', 'rating', 'review_count',
            'category', 'category_name', 'brand', 'brand_name',
            'images', 'variants', 'is_in_stock', 'average_rating',
            'meta_title', 'meta_description', 'created_at',
        )


class ProductRelatedSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    image = FlexibleImageField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'price', 'old_price', 'image', 'category_name', 'rating', 'average_rating')
