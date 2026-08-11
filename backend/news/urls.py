from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.NewsViewSet, basename='news')

admin_router = DefaultRouter()
admin_router.register('', views.AdminNewsViewSet, basename='admin-news')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', include(admin_router.urls)),
]
