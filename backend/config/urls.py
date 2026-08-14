from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/categories/', include('categories.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/favorites/', include('favorites.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/common/', include('common.urls')),
    path('api/news/', include('news.urls')),
    path('api/gallery/', include('gallery.urls')),
    path('api/certificates/', include('certificates.urls')),
    path('api/pages/', include('pages.urls')),
    path('api/contacts/', include('contacts.urls')),
    path('api/support/', include('support.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
