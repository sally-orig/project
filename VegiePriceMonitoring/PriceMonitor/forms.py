from django import forms
from .models import Vegetable

class VegetableForm(forms.ModelForm):
    class Meta:
        model = Vegetable
        fields = ['name', 'description', 'price', 'img']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100px;'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'img': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['img'].widget.attrs['readonly'] = True
            self.fields['name'].required = False
            self.fields['img'].required = False

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Vegetable.objects.filter(name=name).exists() and not self.instance.pk:
            raise forms.ValidationError("A vegetable with this name already exists.")
        return name
