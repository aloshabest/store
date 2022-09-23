from django.shortcuts import render, get_object_or_404
from .models import *


def top_category(request):
    template = 'magazine/index.html'
    categories = Category.objects.filter(parent_id=None)
    products = Product.objects.all()

    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, template, context)