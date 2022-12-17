from .models import *
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.core.paginator import Paginator
from .cart import *
from .favourite import *


class Index(ListView):
    model = Product
    template_name = 'magazine/index.html'
    context_object_name = 'products'
    extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent_id=None)
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get("types") != None:
            price = get_object_or_404(Product, slug=request.POST.get("sl")).price
            return remove_from_cart(request, request.POST.get("sl"), price)
        elif request.POST.get("coupon") != None:
            return add_coupon(request)
        elif request.POST.get("favour") != None:
            return add_or_remove_favourite(request, request.POST.get("sl"))
        else:
            price = get_object_or_404(Product, slug=request.POST.get("sl")).price
            return add_to_cart(request, request.POST.get("sl"), price)


class Contact(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'magazine/contact.html', context={
        })


class Single(DetailView):
    model = Product
    template_name = 'magazine/single_product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'prod_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, prod_slug, *args, **kwargs):
        if request.POST.get("types") != None:
            price = get_object_or_404(Product, slug=request.POST.get("sl")).price
            return remove_from_cart(request, request.POST.get("sl"), price)
        elif request.POST.get("coupon") != None:
            return add_coupon(request)
        elif request.POST.get("favour") != None:
            return add_or_remove_favourite(request, prod_slug)
        else:
            price = get_object_or_404(Product, slug=request.POST.get("sl")).price
            return add_to_cart(request, prod_slug, price)


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

        sale, sale_prod = [i.prod for i in Sale.objects.all()], Sale.objects.all()

        context = {
            'res': res,
            'sale': sale,
            'show': show,
            'type': type,
            'category': category,
            'count': count,
            'page_obj': page_obj,
        }
        return render(request, template, context)

    def post(self, request, *args, **kwargs):
        if request.POST.get("types") != None:
            price = get_object_or_404(Product, slug=request.POST.get("sl")).price
            return remove_from_cart(request, request.POST.get("sl"), price)
        elif request.POST.get("coupon") != None:
            return add_coupon(request)
        elif request.POST.get("favour") != None:
            return add_or_remove_favourite(request, request.POST.get("sl"))
        else:
            price = get_object_or_404(Product, slug=request.POST.get("sl")).price
            return add_to_cart(request, request.POST.get("sl"), price)


class Search(ListView):
    template_name = 'magazine/search.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        return Product.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        context['sale'] = [i.prod for i in Sale.objects.all()]
        context['sale_prod'] = Sale.objects.all()
        context['count'] = context['products'].count()
        return context


class Favourite(View):
    def get(self, request, *args, **kwargs):
        template = 'magazine/favourite.html'

        favourite = request.session.get('favourite')
        products = Product.objects.filter(slug__in=favourite)

        count = products.count()

        paginator = Paginator(products, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        sale, sale_prod = [i.prod for i in Sale.objects.all()], Sale.objects.all()

        context = {
            'sale': sale,
            'count': count,
            'page_obj': page_obj,
            'sale_prod': sale_prod,
        }
        return render(request, template, context)