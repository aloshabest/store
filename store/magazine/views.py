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
    product = get_object_or_404(Product, slug=prod_slug)

    context = {
        'product': product,
    }
    return render(request, template, context)


def shop(request):
    template = 'magazine/shop.html'
    product = Product.objects.all()
    res = [(cat, Category.objects.filter(parent_id=cat)) for cat in Category.objects.filter(parent_id=None)]

    # cat = Category.objects.filter(parent_id=None)
    # ls = []
    # for i in cat:
    #     c = Category.objects.filter(parent_id=cat)
    #     ls.append(c)


    context = {
        'res': res,
    }
    return render(request, template, context)