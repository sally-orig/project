from django.db import models
from django.core.validators import MinValueValidator
    
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('add_vegetable', 'Add Vegetable'),
        ('update_price', 'Update Price'),
        ('delete_vegetable', 'Delete Vegetable'),
        ('add_user', 'Add User'),
    ]
    tran_type = models.CharField(max_length=100, choices=TRANSACTION_TYPES)
    vegetable_name = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], null=True)
    details = models.CharField(max_length=1000)
    location_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.id}'
    
class Vegetable(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    created_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    img = models.ImageField(upload_to='veg_images', blank=False, null=False)
    tran_id = models.ForeignKey('Transaction', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name
    