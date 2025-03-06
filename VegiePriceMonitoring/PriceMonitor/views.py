from django.http import HttpResponse
from django.template import loader

def all_veg_prices(request):
    template = loader.get_template('all_veg_prices.html')
    return HttpResponse(template.render())
