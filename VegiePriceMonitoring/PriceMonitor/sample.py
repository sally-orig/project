from datetime import datetime, timedelta
from .models import Transaction

def create_bulk():
    data = []
    prices = [1, 2, 3, -2, 10, 5, 4, 6, 7, -2, -5, -10, 5, 3, -1, 8, 9, -5]
    for idx, item in enumerate(prices):
        data.append(
            {
            'tran_type': 'update_vegetable',
            'vegetable_name': 'Kamatis',
            'price': 20 + item,
            'created_by': 'sgano',
            'created_at': datetime.now() + timedelta(days=idx)
            }
        )

    for entry in data:
        Transaction.objects.create(**entry)

