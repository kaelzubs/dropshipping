from decimal import Decimal
from catalog.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id, quantity=1):
        product = Product.objects.get(id=product_id)
        item = self.cart.get(str(product_id), {'quantity': 0, 'price': str(product.price), 'title': product.title})
        item['quantity'] += quantity
        self.cart[str(product_id)] = item
        self.save()

    def remove(self, product_id):
        self.cart.pop(str(product_id), None)
        self.save()

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def items(self):
        product_ids = [int(pid) for pid in self.cart.keys()]
        products = Product.objects.filter(id__in=product_ids)
        for p in products:
            data = self.cart[str(p.id)]
            yield {
                'product': p,
                'quantity': data['quantity'],
                'price': Decimal(data['price']),
                'line_total': Decimal(data['price']) * data['quantity'],
            }

    def totals(self):
        subtotal = sum(Decimal(i['price']) * i['quantity'] for i in self.items())
        shipping = Decimal('0')  # flat or calculated later
        total = subtotal + shipping
        return {'subtotal': subtotal, 'shipping': shipping, 'total': total}