from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .cart import Cart
from .forms import CheckoutForm
from .models import Order, OrderItem, Address
from catalog.models import Product
import stripe
import os
from django.conf import settings
from pathlib import Path
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

# stripe.api_key =  'STRIPE_API_KEY'  # env var in production
stripe.api_key = os.getenv('STRIPE_API_KEY')

def cart_item_count(request):
    cart = request.session.get('cart', {})
    count = sum(item['quantity'] for item in cart.values()) if cart else 0
    return {'cart_item_count': count}

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'orders/cart.html', {'cart_items': list(cart.items()), 'totals': cart.totals()})

def cart_add(request, product_id):
    cart = Cart(request)
    if request.method == 'POST':
        qty = int(request.POST.get('quantity', 1))
        cart.add(product_id, qty)
    return redirect('orders:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('orders:cart_detail')

def checkout(request):
    cart = Cart(request)
    items = list(cart.items())
    totals = cart.totals()
    if not items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('catalog:list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            addr = form.save(commit=False)
            if request.user.is_authenticated:
                addr.user = request.user
            addr.save()

            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                email=request.user.email if request.user.is_authenticated else request.POST.get('email', ''),
                shipping_address=addr,
                subtotal=totals['subtotal'],
                shipping_cost=totals['shipping'],
                total=totals['total'],
            )
            for i in items:
                OrderItem.objects.create(
                    order=order, product=i['product'], quantity=i['quantity'], unit_price=i['price']
                )

            # Create Stripe PaymentIntent (simple example)
            intent = stripe.PaymentIntent.create(
                amount=int(totals['total'] * 100),  # in kobo/cent
                currency='ngn',
                metadata={'order_id': order.id},
            )
            order.stripe_payment_intent = intent['id']
            order.save()

            cart.clear()
            return redirect('orders:success', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'orders/checkout.html', {'form': form, 'cart_items': items, 'totals': totals})

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/success.html', {'order': order})