from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.CategoryViewSet, basename='category')

admin_router = DefaultRouter()
admin_router.register('', views.AdminCategoryViewSet, basename='admin-category')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', include(admin_router.urls)),
]
