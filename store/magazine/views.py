from django.shortcuts import render, get_object_or_404
from .models import *


def index(request):
    template = 'magazine/index.html'
    categories = Category.objects.filter(parent_id=None)
    products = Product.objects.all()

    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, template, context)


def single(request, prod_slug):
    template = 'magazine/single_product.html'
    #template = 'magazine/single-product-details.html'
    product = get_object_or_404(Product, slug=prod_slug)

    context = {
        'product': product,
    }
    return render(request, template, context)