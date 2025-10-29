from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


def product_list(request):
    products = Product.objects.filter(is_active=True).order_by('-id')
    categories = Category.objects.all()
    
    # products = Product.objects.all().order_by('-id')   # or any ordering you prefer
    paginator = Paginator(products, 4)  # 12 products per page
    page_number = request.GET.get("page")
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'catalog/list.html', {'products': products, 'categories': categories, 'page_obj': page_obj})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'catalog/detail.html', {'product': product})


def search_product(request):
    query = request.GET.get("q", "")
    products = Product.objects.all()

    if query:
        products = products.filter(Q(title__icontains=query) |
                                   Q(description__icontains=query)).distinct() # adjust field as needed

    paginator = Paginator(products, 1)  # 12 results per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
        
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'catalog/search.html', {'products': products, 'query': query, 'page_obj': page_obj})