from django.shortcuts import render, get_object_or_404
from .models import *
from django.shortcuts import render
from django.views import View


class Index(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(parent_id=None)
        products = Product.objects.all()
        return render(request, 'magazine/index.html', context={
            'categories': categories,
            'products': products,
        })


class Single(View):

    def get(self, request, prod_slug, *args, **kwargs):
        product = get_object_or_404(Product, slug=prod_slug)
        return render(request, 'magazine/single_product.html', context={
            'product': product,
        })


def shop(request):
    template = 'magazine/shop.html'
    product = Product.objects.all()
    res = [(cat, Category.objects.filter(parent_id=cat)) for cat in Category.objects.filter(parent_id=None)]

    context = {
        'res': res,
    }
    return render(request, template, context)