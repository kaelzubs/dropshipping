from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q


def product_list(request):
    products = Product.objects.filter(is_active=True).order_by('-id')
    categories = Category.objects.all()
    
    # products = Product.objects.all().order_by('-id')   # or any ordering you prefer
    paginator = Paginator(products, 4)  # 12 products per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog/list.html', {'products': products, 'categories': categories, 'page_obj': page_obj})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'catalog/detail.html', {'product': product})


def search_product(request):
    query = request.GET.get('q', '').strip()
    if not query:
        products = Product.objects.none()
    else:
        products = Product.objects.filter(
            is_active=True
        ).filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).distinct()
        
    paginator = Paginator(products, 4)  # 12 products per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog/search.html', {'products': products, 'query': query, 'page_obj': page_obj})