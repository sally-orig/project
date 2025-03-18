from django.template import loader
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .models import Vegetable, Transaction
from .forms import VegetableForm

def price_list(request):
    query = request.GET.get('query', '')
    if query:
        vegetables = Vegetable.objects.filter(name__icontains=query)
    else:
        vegetables = Vegetable.objects.select_related('tran_id').all().order_by('name')

    template = loader.get_template('pricelist.html')
    context = {
        'vegetables': vegetables
    }
    return HttpResponse(template.render(context, request))

def add_vegetable(request):
    if request.method == 'POST' and request.FILES['img']:
        add_veg_form = VegetableForm(request.POST, request.FILES)
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
        add_veg_form = VegetableForm()

    template = loader.get_template('addvegetable.html')
    context = {
        'form': add_veg_form
    }
    return HttpResponse(template.render(context, request))

def update_vegetable(request, pk: int = None):
    veg_instance = get_object_or_404(Vegetable, pk=pk)

    if request.method == 'POST':
        update_veg_form = VegetableForm(request.POST, request.FILES, instance=veg_instance)
        if update_veg_form.is_valid():
            vegetable = update_veg_form.save(commit=False)
            transaction = Transaction.objects.create(
                tran_type='update_price', 
                details=f'Update vegetable',
            )

            vegetable.tran_id = transaction
            vegetable.save()
            return redirect('price_list')
    else:
        update_veg_form = VegetableForm(instance=veg_instance)

    template = loader.get_template('updatevegetable.html')
    context = {
        'form': update_veg_form
    }
    return HttpResponse(template.render(context, request))

def delete_vegetable(request, pk: int = None):
    veg_instance = get_object_or_404(Vegetable, pk=pk)
    veg_instance.delete()
    return redirect('price_list')