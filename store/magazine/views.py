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


def shop(request, cat_slug):

    template = 'magazine/shop.html'
    res = [(cat, Category.objects.filter(parent_id=cat)) for cat in Category.objects.filter(parent_id=None)]

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if cat_slug:
        category = get_object_or_404(Category, slug=cat_slug)
        products = Product.objects.filter(category=category)

    context = {
        'res': res,
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, template, context)


# def shop_all(request, indx):
#     template = 'magazine/shop.html'
#     res = [(cat, Category.objects.filter(parent_id=cat)) for cat in Category.objects.filter(parent_id=None)]
#
#     if indx == 'all':
#         products = Product.objects.filter(available=True)
#
#     else:
#         category = indx
#
#         sub1 = list(Category.objects.filter(parent=category))
#         sub2 = list(Category.objects.filter(parent__in=sub1))
#         #  можешь в цикле набрать нужное количество вложенностей
#
#         products = Product.objects.filter(category__in=sub1 + sub2)
#
#
#     context = {
#         'res': res,
#         'products': products,
#     }
#     return render(request, template, context)

