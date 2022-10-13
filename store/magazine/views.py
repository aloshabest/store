from django.shortcuts import render, get_object_or_404
from .models import *
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.core.paginator import Paginator


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


# class ShopWomen(View):
#     def get(self, request, cat_slug, *args, **kwargs):
#
#         template = 'magazine/shop.html'
#         res = [(cat, Category.objects.filter(parent_id=cat)) for cat in Category.objects.filter(parent_id=None)]
#
#         category = get_object_or_404(Category, slug=cat_slug)
#         products = Product.objects.filter(category=category, type='Women')
#         show = Category.objects.filter(id=category.parent_id)
#
#         if category.parent_id == None:
#             sub1 = list(Category.objects.filter(parent=category))
#             sub2 = list(Category.objects.filter(parent__in=sub1))
#
#             products = Product.objects.filter(category__in=sub1 + sub2, type='Women')
#
#         context = {
#             'res': res,
#             'products': products,
#             'show': show,
#         }
#         return render(request, template, context)
#
#
# class ShopMen(View):
#     def get(self, request, cat_slug, *args, **kwargs):
#
#         template = 'magazine/shop.html'
#         res = [(cat, Category.objects.filter(parent_id=cat)) for cat in Category.objects.filter(parent_id=None)]
#
#         category = get_object_or_404(Category, slug=cat_slug)
#         products = Product.objects.filter(category=category, type='Men')
#         show = Category.objects.filter(id=category.parent_id)
#
#         if category.parent_id == None:
#             sub1 = list(Category.objects.filter(parent=category))
#             sub2 = list(Category.objects.filter(parent__in=sub1))
#
#             products = Product.objects.filter(category__in=sub1 + sub2, type='Men')
#
#         context = {
#             'res': res,
#             'products': products,
#             'show': show,
#         }
#         return render(request, template, context)

class Shop(View):
    def get(self, request, type, cat_slug, *args, **kwargs):
        template = 'magazine/shop.html'

        # список из общих категорий, проходящих по гендеру и подкатегорий основных категорий
        res = [(cat, Category.objects.filter(parent_id=cat, type=type)) for cat in Category.objects.filter(parent_id=None, type__in=(type, 'all'))]

        # категория по слагу и продукты по этой категории
        category = get_object_or_404(Category, slug=cat_slug)
        products = Product.objects.filter(category=category)

        # открывает шторку выбранной категории в списке
        show = Category.objects.filter(id=category.parent_id)

        # показать все продукты по общей категории
        if category.parent_id == None:
            sub1 = list(Category.objects.filter(parent=category, type=type))
            sub2 = list(Category.objects.filter(parent__in=sub1))
            products = Product.objects.filter(category__in=sub1 + sub2)

            show = Category.objects.filter(title=category)

        count = products.count()

        paginator = Paginator(products, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'res': res,
            'products': products,
            'show': show,
            'type': type,
            'category': category,
            'count': count,
            'page_obj':page_obj,
        }
        return render(request, template, context)