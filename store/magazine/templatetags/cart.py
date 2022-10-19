from django import template
from magazine.models import Cart
import random
from django.db.models import Count


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