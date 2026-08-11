from django.db import models


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=255, default='Shirinliklar Dunyosi')
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=15000)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
