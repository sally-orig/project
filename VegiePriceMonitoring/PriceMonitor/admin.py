from django.contrib import admin
from django import forms
from .models import Vegetable, VegetableAction

class VegetableAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'created_at', 'status', 'get_tran_id')

    def get_tran_id(self, obj):
        return obj.tran_id.id
    
    get_tran_id.short_description = 'Tran ID'

class VegetableActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'tran_type', 'created_at', 'created_by', 'details')

admin.site.register(Vegetable, VegetableAdmin)
admin.site.register(VegetableAction, VegetableActionAdmin)
