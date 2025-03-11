from django.template import loader
from django.http import HttpResponse

def price_list(request):
    template = loader.get_template('pricelist.html')
    context = {
        'vegetables': [
            {'name': 'Tomato', 'price': 10.5, 'updated_at': '2021-10-01 12:00:00'},
            {'name': 'Potato', 'price': 25, 'updated_at': '2021-10-01 12:00:00'},
            {'name': 'Onion', 'price': 199, 'updated_at': '2021-10-01 12:00:00'}
        ],
    }
    return HttpResponse(template.render(context, request))