from django.template import loader
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Vegetable, Transaction
from .forms import AddVegForm

def price_list(request):
    vegetables = Vegetable.objects.all().values('name', 'price', 'img')
    template = loader.get_template('pricelist.html')
    context = {
        'vegetables': vegetables
    }
    return HttpResponse(template.render(context, request))

def add_vegetable(request):
    if request.method == 'POST' and request.FILES['img']:
        add_veg_form = AddVegForm(request.POST, request.FILES)
        if add_veg_form.is_valid():
            vegetable = add_veg_form.save(commit=False)
            transaction = Transaction.objects.create(
                tran_type='add_vegetable', 
                details=f'Add new vegetable',
                )

            vegetable.tran_id = transaction
            vegetable.save()
            return redirect('price_list')
    else:
        add_veg_form = AddVegForm(request.POST, request.FILES)
    return render(request, 'addvegetable.html', {
        'add_veg_form': add_veg_form,
    })