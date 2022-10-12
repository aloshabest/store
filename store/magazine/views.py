from django.shortcuts import render, get_object_or_404
from .models import *
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import F


# class Index(View):
#
#     def get(self, request, *args, **kwargs):
#         categories = Category.objects.filter(parent_id=None)
#         products = Product.objects.all()
#         return render(request, 'magazine/index.html', context={
#             'categories': categories,
#             'products': products,
#         })


class Index(ListView):
    model = Product
    template_name = 'magazine/index.html'
    context_object_name = 'products'
    extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent_id=None)
        return context


# class Single(View):
#
#     def get(self, request, prod_slug, *args, **kwargs):
#         product = get_object_or_404(Product, slug=prod_slug)
#         return render(request, 'magazine/single_product.html', context={
#             'product': product,
#         })

class Single(DetailView):
    model = Product
    template_name = 'magazine/single_product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'prod_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



def shop(request, cat_slug):

    template = 'magazine/shop.html'
    res = [(cat, Category.objects.filter(parent_id=cat)) for cat in Category.objects.filter(parent_id=None)]

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if cat_slug:
        category = get_object_or_404(Category, slug=cat_slug)
        products = Product.objects.filter(category=category)

        if category.parent_id == None:
            sub1 = list(Category.objects.filter(parent=category))
            sub2 = list(Category.objects.filter(parent__in=sub1))

            products = Product.objects.filter(category__in=sub1 + sub2)

    context = {
        'res': res,
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, template, context)

