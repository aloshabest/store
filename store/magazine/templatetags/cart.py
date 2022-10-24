from django import template
from magazine.models import Cart, Product
import random
from django.db.models import Count
from decimal import Decimal
from django.shortcuts import get_object_or_404


register = template.Library()


@register.inclusion_tag('magazine/header_cart_tpl.html')
def header_cart_area(session):
    context = {
    }
    cart = session.get('cart', None)

    if cart:
        context['count'] = cart['count']
    return context


@register.inclusion_tag('magazine/cart_tpl.html')
def cart_area(session):
    context = {
    }
    cart = session.get('cart', None)

    if cart:
        context['cart'] = cart
        context['count'] = cart['count']

        prod = [(get_object_or_404(Product, slug=k), int(v['quantity'])) for k, v in cart.items() if k != 'subtotal' and k != 'count']

        context['prod'] = prod

        subtotal = cart['subtotal']
        discount = float(15)
        total = subtotal - subtotal * (discount / 100)

        context['subtotal'] = subtotal
        context['discount'] = discount
        context['total'] = total

    return context
