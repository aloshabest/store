from django import template
from magazine.models import Cart, Product
import random
from django.db.models import Count
from decimal import Decimal


register = template.Library()


@register.inclusion_tag('magazine/header_cart_tpl.html')
def header_cart_area(session):
    context = {
    }
    cart = session.get('cart', None)

    if cart:
        count = 0
        for v in cart.values():
            count += int(v['quantity'])
        context['count'] = count

    return context


@register.inclusion_tag('magazine/cart_tpl.html')
def cart_area(session):
    context = {
    }
    cart = session.get('cart', None)

    if cart:
        context['cart'] = cart

        count = 0
        for v in cart.values():
            count += int(v['quantity'])
        context['count'] = count

        prod = [Product.objects.filter(slug=k) for k in cart.keys()]
        context['prod'] = prod

        subtotal = Decimal()
        discount = Decimal(15)
        for item in prod:
            for p in item:
                subtotal += p.price
        total = subtotal - subtotal * (discount / 100)

        context['subtotal'] = subtotal
        context['discount'] = discount
        context['total'] = total

    return context
