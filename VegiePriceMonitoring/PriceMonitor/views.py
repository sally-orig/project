from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q, Avg, Count, functions
from datetime import datetime
import requests
import os
from django.http import Http404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Vegetable, VegetableAction
from .forms import VegetableForm


TRAN_TYPE_UPDATE: str = 'update_price'
TRAN_TYPE_ADD: str = 'add_vegetable'

BASE_API_URL: str = "http://127.0.0.1:8001"
VEGETABLES_API_URL: str = f"{BASE_API_URL}/vegetables"
VEGETABLE_ACTIONS_API_URL: str = f"{BASE_API_URL}/vegetable-actions"
VEGETABLE_PRICE_CHART_API_URL: str = f"{BASE_API_URL}/vegetable-price-chart"

def is_admin_or_staff(user):
    return user.groups.filter(name='admin').exists()

def price_list(request):
    query = request.GET.get('query', None)
    response = requests.get(VEGETABLES_API_URL, params={'query': query})

    if response.status_code == 200:
        vegetables = response.json()
    else:
        vegetables = []

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
    UPLOADED_IMAGES_FOLDER: str = "veg_images"
    if request.method == 'POST' and 'img' in request.FILES:
        add_veg_form = VegetableForm(request.POST, request.FILES)
        if add_veg_form.is_valid():
            img = request.FILES['img']
            folder_path = os.path.join(settings.MEDIA_ROOT, UPLOADED_IMAGES_FOLDER)
            fs = FileSystemStorage(location=folder_path)
            filename = fs.save(img.name, img)
            img_url = f"{UPLOADED_IMAGES_FOLDER}/{filename}"
            vegetable_data = {
                'name': add_veg_form.cleaned_data['name'],
                'price': float(add_veg_form.cleaned_data['price']),
                'img': img_url,
                'description': add_veg_form.cleaned_data['description'],
                'created_by': str(request.user),
            }
            response = requests.post(VEGETABLES_API_URL, json=vegetable_data)
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
    response = requests.delete(f"{VEGETABLES_API_URL}/{pk}", json={'updated_by': str(request.user)})
    if response.status_code == 404:
        raise Http404("Vegetable not found.")
    elif response.status_code == 500:
        return render(request, '500.html', {'message': 'Server error occurred.'})
    return redirect('price_list')

@user_passes_test(is_admin_or_staff)
def vegetable_actions_log(request):
    response = requests.get(VEGETABLE_ACTIONS_API_URL)
    if response.status_code == 200:
        actions = response.json()
        for action in actions:
            action['price'] = round(float(action['price']), 2)
    else:
        actions = []
    context = {
        'actions': actions
    }
    return render(request, 'vegetableactionslog.html', context)

def veg_price_chart(request):
    # Prepare price data for each vegetable
    chart_data = {
        'labels': [],  # Dates for x-axis
        'datasets': [] 
    }

    vegetables = requests.get(VEGETABLES_API_URL).json()
    selected_vegetable = request.GET.get('vegetable', 'Kamatis')
    response = requests.get(VEGETABLE_PRICE_CHART_API_URL, params={'selected_vegetable': selected_vegetable})
    if response.status_code == 200:
        dates = response.json().get('dates', [])
        prices = response.json().get('prices', [])
        highest_price = response.json().get('highest_price', {})
        lowest_price = response.json().get('lowest_price', {})
        max_price = float(response.json().get('max_price', 0))

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
            'highest_price_data': highest_price,
            'lowest_price_data': lowest_price
        }

        return render(request, 'vegpricechart.html', context)
    else:
        return render(request, '500.html', {'error': 'Failed to fetch data from the API.'})