from rest_framework import serializers
from .models import GalleryCategory, GalleryImage


class GalleryCategorySerializer(serializers.ModelSerializer):
    image_count = serializers.SerializerMethodField()

    class Meta:
        model = GalleryCategory
        fields = ('id', 'name', 'slug', 'image_count')

    def get_image_count(self, obj):
        return obj.images.count()


class GalleryImageSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True, default='')

    class Meta:
        model = GalleryImage
        fields = ('id', 'title', 'description', 'image', 'category', 'category_name', 'is_featured', 'order', 'created_at')
