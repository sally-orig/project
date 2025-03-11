from django.db import models

class Vegetable(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    img = models.ImageField(upload_to='veg_images', blank=False, null=False)

    def __str__(self):
        return self.name
