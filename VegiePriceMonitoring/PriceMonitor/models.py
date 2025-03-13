from django.db import models
    
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('add_vegetable', 'Add Vegetable'),
        ('update_price', 'Update Price'),
        ('add_user', 'Add User'),
    ]
    tran_type = models.CharField(max_length=100, choices=TRANSACTION_TYPES)
    details = models.CharField(max_length=1000)
    location_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.id}'
    
class Vegetable(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    img = models.ImageField(upload_to='veg_images', blank=False, null=False)
    tran_id = models.ForeignKey('Transaction', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name
    
class PriceHistory(models.Model):
    vegetable_id = models.IntegerField(null=False)
    location_id = models.IntegerField(null=False)
    created_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)