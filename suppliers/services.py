import requests
from .models import SupplierOrder, Supplier
from orders.models import Order

def send_order_to_supplier(order: Order, supplier: Supplier):
    payload = {
        'order_id': order.id,
        'customer': {
            'name': order.shipping_address.full_name,
            'address': {
                'line1': order.shipping_address.line1,
                'line2': order.shipping_address.line2,
                'city': order.shipping_address.city,
                'state': order.shipping_address.state,
                'postcode': order.shipping_address.postcode,
                'country': order.shipping_address.country,
            },
            'phone': order.shipping_address.phone,
            'email': order.email,
        },
        'items': [
            {'sku': i.product.supplier_sku, 'qty': i.quantity}
            for i in order.items.all()
        ]
    }

    so = SupplierOrder.objects.create(
        supplier=supplier, local_order_id=order.id, payload=payload, status='created'
    )

    headers = {'Authorization': f'Bearer {supplier.api_key}', 'Content-Type': 'application/json'}
    try:
        resp = requests.post(f'{supplier.base_url}/orders', json=payload, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        so.remote_order_id = data.get('id', '')
        so.status = 'submitted'
        order.status = 'sent_to_supplier'
        order.save()
    except Exception:
        so.status = 'error'
    finally:
        so.save()
    return so