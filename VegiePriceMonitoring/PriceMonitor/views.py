from django.template import loader
from django.http import HttpResponse
from .models import Vegetable

def price_list(request):
    vegetables = Vegetable.objects.all().values('name', 'price', 'updated_at', 'img')
    template = loader.get_template('pricelist.html')
    context = {
        'vegetables': vegetables
    }
    return HttpResponse(template.render(context, request))