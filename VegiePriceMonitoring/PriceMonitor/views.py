from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Vegetable, Transaction
from .forms import VegetableForm

def is_admin_or_staff(user):
    return user.groups.filter(name='admin').exists()

def price_list(request):
    query = request.GET.get('query', '')
    if query:
        vegetables = Vegetable.objects.filter(name__icontains=query, status=True).order_by('name')
    else:
        vegetables = Vegetable.objects.select_related('tran_id').filter(status=True).order_by('name')

    is_admin = request.user.groups.filter(name='admin').exists()
    context = {
        'vegetables': vegetables,
        'is_admin': is_admin 
    }
    return render(request, 'pricelist.html', context)

def save_transaction_logs(user, details: VegetableForm, tran_type: str, otherDetails: str) -> Transaction:
    transaction = Transaction.objects.create(
        tran_type=tran_type, 
        details=otherDetails,
        vegetable_name=details.name,
        price=details.price,
        created_by=user
    )
    return transaction

@user_passes_test(is_admin_or_staff)
def add_vegetable(request):
    if request.method == 'POST' and 'img' in request.FILES:
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

    context = {
        'form': add_veg_form
    }
    return render(request, 'addvegetable.html', context)

@user_passes_test(is_admin_or_staff)
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

    context = {
        'form': update_veg_form
    }
    return render(request, 'updatevegetable.html', context)

@user_passes_test(is_admin_or_staff)
def delete_vegetable(request, pk: int = None):
    veg_instance = get_object_or_404(Vegetable, pk=pk)
    transaction = save_transaction_logs(request.user, veg_instance, 'delete_vegetable', f'Delete Vegetable {veg_instance.name}')
    veg_instance.tran_id = transaction
    veg_instance.status = False
    veg_instance.save()
    return redirect('price_list')

@user_passes_test(is_admin_or_staff)
def transaction_log(request):
    transactions = Transaction.objects.all().order_by('created_at').reverse()
    context = {
        'transactions': transactions
    }
    return render(request, 'transactionlog.html', context)
