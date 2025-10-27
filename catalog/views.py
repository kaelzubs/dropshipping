from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.contrib.auth.decorators import login_required

@login_required
def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    return render(request, 'catalog/list.html', {'products': products, 'categories': categories})

@login_required
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'catalog/detail.html', {'product': product})