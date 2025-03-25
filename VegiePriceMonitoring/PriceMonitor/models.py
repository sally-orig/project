from django.db import models
from django.core.validators import MinValueValidator
    
class VegetableAction(models.Model):
    ACTION_TYPES = [
        ('add_vegetable', 'Add Vegetable'),
        ('update_price', 'Update Price'),
        ('deactivate_vegetable', 'Deactivate Vegetable'),
    ]
    tran_type = models.CharField(max_length=100, choices=ACTION_TYPES)
    vegetable_name = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], null=True)
    details = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now=False)
    created_by = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.id}'
    
class Vegetable(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    created_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=False)
    status = models.BooleanField(default=True)
    img = models.ImageField(upload_to='veg_images', blank=False, null=False)
    tran_id = models.ForeignKey('VegetableAction', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name
    