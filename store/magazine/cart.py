from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import *


def add_to_cart(request, prod_slug):
    prod = get_object_or_404(Product, slug=prod_slug)

    if 'cart' not in request.session:
        request.session['cart'] = {}

    cart = request.session.get('cart')
    if prod_slug in cart:
        cart[prod_slug]['quantity'] += 1

    else:
        cart[prod_slug] = {
            'quantity': 1,
        }
    request.session.modified = True

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request, prod_slug):
    cart = request.session.get('cart')

    cart[prod_slug]['quantity'] -= 1

    if cart[prod_slug]['quantity'] == 0:
        del cart[prod_slug]

    request.session.modified = True

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))