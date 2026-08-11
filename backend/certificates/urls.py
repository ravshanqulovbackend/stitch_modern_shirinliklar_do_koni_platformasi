from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.CertificateViewSet, basename='certificate')

admin_router = DefaultRouter()
admin_router.register('', views.AdminCertificateViewSet, basename='admin-certificate')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', include(admin_router.urls)),
]
