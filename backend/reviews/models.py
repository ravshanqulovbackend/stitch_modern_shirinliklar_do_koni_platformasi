from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - {self.product} ({self.rating})'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._update_product_rating()

    def _update_product_rating(self):
        from django.db.models import Avg
        agg = Review.objects.filter(product=self.product).aggregate(avg=Avg('rating'))
        self.product.rating = round(agg['avg'] or 0, 1)
        self.product.review_count = Review.objects.filter(product=self.product).count()
        self.product.save(update_fields=['rating', 'review_count'])
