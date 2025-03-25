from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q, Avg, Count, functions
from datetime import datetime
from .models import Vegetable, VegetableAction
from .forms import VegetableForm


TRAN_TYPE_UPDATE: str = 'update_price'
TRAN_TYPE_ADD: str = 'add_vegetable'

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

def save_transaction_logs(user, details: VegetableForm, tran_type: str, otherDetails: str) -> VegetableAction:
    transaction = VegetableAction.objects.create(
        tran_type=tran_type, 
        details=otherDetails,
        vegetable_name=details.name,
        price=details.price,
        created_by=user,
        created_at=datetime.now()
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
                vegetable.created_at = datetime.now()
                vegetable.save()
                transaction = save_transaction_logs(request.user, vegetable, 'add_vegetable', f'Vegetable {vegetable.name} reactivated')
            else:
                vegetable = add_veg_form.save(commit=False)
                transaction = save_transaction_logs(request.user, vegetable, 'add_vegetable', f'Add Vegetable {vegetable.name}')
                vegetable.tran_id = transaction
                vegetable.created_by = request.user
                vegetable.created_at = datetime.now()
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
            vegetable.created_at = datetime.now()
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
    transaction = save_transaction_logs(request.user, veg_instance, 'deactivate_vegetable', f'Deactivate Vegetable {veg_instance.name}')
    veg_instance.tran_id = transaction
    veg_instance.status = False
    veg_instance.save()
    return redirect('price_list')

@user_passes_test(is_admin_or_staff)
def vegetable_actions_log(request):
    vegetable_actions = VegetableAction.objects.all().order_by('created_at').reverse()
    context = {
        'actions': vegetable_actions
    }
    return render(request, 'vegetableactionslog.html', context)

def veg_price_chart(request):
    # Prepare price data for each vegetable
    chart_data = {
        'labels': [],  # Dates for x-axis
        'datasets': [] 
    }
    max_price = 0
    dates = []
    prices = []

    vegetables = Vegetable.objects.values('name').all()
    selected_vegetable = request.GET.get('vegetable', 'Kamatis')

    price_updates = (
        VegetableAction.objects
        .filter(Q(tran_type='add_vegetable') | Q(tran_type='update_price'), vegetable_name=selected_vegetable)
        .annotate(date=functions.TruncDate('created_at'))
        .values('date')
        .distinct()
        .annotate(average_price=Avg('price'))
        .order_by('date')
    )
    for update in price_updates:
        dates.append(update['date'].strftime('%b %d, %Y'))
        prices.append(float(update['average_price']))

        if update['average_price'] > max_price:
            max_price = update['average_price']

    if dates and prices:
        chart_data['labels'] = dates
        chart_data['datasets'].append({
            'label': selected_vegetable, 
            'data': prices,
            'fill': 'false',
            'borderColor': '#4CAF50',
            'tension': 0.1,
            'pointStyle': 'circle',
            'pointRadius': 5,
            'pointBackgroundColor': 'gray'
        })
    is_admin = request.user.groups.filter(name='admin').exists()
    context = {
        'chart_data': chart_data,
        'is_admin': is_admin,
        'dynamic_y_max': max_price + 10,
        'vegetables': vegetables,
        'selected_vegetable': selected_vegetable,
    }

    return render(request, 'vegpricechart.html', context)