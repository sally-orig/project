from django.template import loader
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .models import Vegetable, Transaction
from .forms import VegetableForm

def price_list(request):
    query = request.GET.get('query', '')
    if query:
        vegetables = Vegetable.objects.filter(name__icontains=query, status=True).order_by('name')
    else:
        vegetables = Vegetable.objects.select_related('tran_id').filter(status=True).order_by('name')

    template = loader.get_template('pricelist.html')
    context = {
        'vegetables': vegetables
    }
    return HttpResponse(template.render(context, request))

def save_transaction_logs(user, details: VegetableForm, tran_type: str, otherDetails: str) -> Transaction:
    transaction = Transaction.objects.create(
        tran_type=tran_type, 
        details=otherDetails,
        vegetable_name=details.name,
        price=details.price,
        created_by=user
    )
    return transaction


def add_vegetable(request):
    if request.method == 'POST':
        if 'img' in request.FILES:
            add_veg_form = VegetableForm(request.POST, request.FILES)
            if add_veg_form.is_valid():
                vegetable_name = add_veg_form.cleaned_data['name']
                vegetable = Vegetable.objects.filter(name=vegetable_name).first()
                if vegetable:
                    vegetable.status = True
                    vegetable.description = add_veg_form.cleaned_data['description']
                    vegetable.price = add_veg_form.cleaned_data['price']
                    vegetable.img = add_veg_form.cleaned_data['img']
                    vegetable.save()
                    transaction = save_transaction_logs(request.user, vegetable, 'add_vegetable', f'Vegetable {vegetable.name} reactivated')
                else:
                    vegetable = add_veg_form.save(commit=False)
                    transaction = save_transaction_logs(request.user, vegetable, 'add_vegetable', f'Add Vegetable {vegetable.name}')
                    vegetable.tran_id = transaction
                    vegetable.created_by = request.user
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
            transaction = save_transaction_logs(request.user, vegetable, 'update_price', f'Update Price of {vegetable.name}')
            vegetable.tran_id = transaction
            vegetable.created_by = str(transaction.created_by)
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
    transaction = save_transaction_logs(request.user, veg_instance, 'delete_vegetable', f'Delete Vegetable {veg_instance.name}')
    veg_instance.tran_id = transaction
    veg_instance.status = False
    veg_instance.save()
    return redirect('price_list')

def transaction_log(request):
    transactions = Transaction.objects.all().order_by('created_at').reverse()

    template = loader.get_template('transactionlog.html')
    context = {
        'transactions': transactions
    }
    return HttpResponse(template.render(context, request))