from django import template
from magazine.models import Cart
import random
from django.db.models import Count
from decimal import Decimal


register = template.Library()

@register.inclusion_tag('magazine/cart_area_tpl.html')
def cart_area(user):
    cart = Cart.objects.all()
    count = Cart.objects.filter(customer=user).count()
    user = user
    return {'cart': cart, 'count': count, 'user': user}


@register.inclusion_tag('magazine/header_cart_area_tpl.html')
def header_cart_area(user):
    count = Cart.objects.filter(customer=user).count()
    return {'count': count}


@register.inclusion_tag('magazine/cart_item_tpl.html')
def cart_item(user):
    cart = Cart.objects.filter(customer=user)
    return {'cart': cart}


@register.inclusion_tag('magazine/summary_tpl.html')
def summary(user):
    cart = Cart.objects.filter(customer=user)
    subtotal = Decimal()
    discount = Decimal(15)
    for c in cart:
        subtotal += c.product.price
    total = subtotal - subtotal * (discount / 100)
    return {'cart': cart, 'subtotal': subtotal, 'discount': discount, 'total': total}