from django.template import loader
from django.http import HttpResponse

def price_list(request):
    template = loader.get_template('pricelist.html')
    context = {
        'data': 'Hello world!',
    }
    return HttpResponse(template.render(context, request))